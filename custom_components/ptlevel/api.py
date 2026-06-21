"""API Client for PTDevices."""

import json
import logging
import re
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)


class PTDevicesAPI:
    """Client for PTDevices cloud API."""

    def __init__(self, username: str, password: str, base_url: str, update_interval: int):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.update_interval = update_interval
        self._session: aiohttp.ClientSession | None = None
        self._authenticated = False

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            jar = aiohttp.CookieJar()
            self._session = aiohttp.ClientSession(
                cookie_jar=jar,
                headers={
                    "User-Agent": "Mozilla/5.0 PTLevel-HA/1.0",
                },
            )
        return self._session

    async def authenticate(self) -> bool:
        """Authenticate with PTDevices using form login.

        Flow:
        1. GET /login to obtain CSRF token and session cookies
        2. POST /login with email, password, and CSRF token
        """
        session = await self._get_session()
        login_url = f"{self.base_url}/login"

        try:
            async with session.get(f"{self.base_url}/login") as resp:
                if resp.status >= 400:
                    _LOGGER.error("Failed to reach PTDevices: %s", resp.status)
                    return False
                page = await resp.text()

            csrf = self._extract_csrf(page)
            if not csrf:
                _LOGGER.error("Could not find CSRF token on PTDevices login page")
                return False

            async with session.post(
                login_url,
                data={
                    "_token": csrf,
                    "email": self.username,
                    "password": self.password,
                },
                allow_redirects=False,
            ) as resp:
                if resp.status in (301, 302) and "home" in str(resp.headers.get("Location", "")):
                    self._authenticated = True
                    _LOGGER.info("Authenticated with PTDevices successfully")
                    return True
                else:
                    body = await resp.text()
                    _LOGGER.error(
                        "PTDevices login failed: status=%s location=%s",
                        resp.status,
                        resp.headers.get("Location", "none"),
                    )

                    if "Invalid credentials" in body or "These credentials" in body:
                        return False
                    return False

        except aiohttp.ClientError as err:
            _LOGGER.error("PTDevices connection error during auth: %s", err)
            return False

    async def fetch_data(self) -> dict[str, Any]:
        """Fetch tank data from PTDevices.

        POST /device/all with session cookies and XMLHttpRequest header.
        CSRF token is only required for login, not for data fetches.
        """
        if not self._authenticated:
            _LOGGER.debug("Not authenticated; attempting login")
            if not await self.authenticate():
                raise PTDevicesAuthError("Authentication failed")

        session = await self._get_session()

        try:
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
            }
            async with session.post(
                f"{self.base_url}/device/all",
                headers=headers,
            ) as resp:
                if resp.status == 401 or resp.status == 403:
                    _LOGGER.info("Session expired; re-authenticating")
                    self._authenticated = False
                    if not await self.authenticate():
                        raise PTDevicesAuthError("Re-authentication failed")
                    return await self.fetch_data()
                if resp.status != 200:
                    raise PTDevicesError(
                        f"Device/all returned {resp.status}: {await resp.text()}"
                    )
                raw_devices = await resp.json()

            devices = []
            for raw in raw_devices:
                sensor_data = []
                try:
                    if isinstance(raw.get("sensor_data"), str):
                        sensor_data = json.loads(raw["sensor_data"])
                except (json.JSONDecodeError, TypeError):
                    pass

                battery_ok = "good" in str(raw.get("batteryStatus", "")).lower()
                status_ok = "working" in str(raw.get("status", "")).lower()

                device = {
                    "id": str(raw.get("id", "")),
                    "name": raw.get("nickname") or f"PTLevel {raw.get('id', '')}",
                    "level_percent": float(raw.get("percentLevel", 0)),
                    "level_inches": float(raw.get("inchLevel", 0)),
                    "volume": float(raw.get("volumeLevel", 0)),
                    "battery_ok": battery_ok,
                    "battery_voltage": self._extract_sensor(sensor_data, "2"),
                    "temperature": self._extract_sensor(sensor_data, "3"),
                    "online": status_ok,
                    "firmware_version": str(raw.get("version", "")),
                    "tx_version": str(raw.get("tx_version", "")),
                    "units": raw.get("units", "imperial"),
                    "device_type": raw.get("device_type", "level"),
                    "local_ip": raw.get("local_ip", ""),
                    "last_updated": raw.get("updated_at", ""),
                    "last_reported": raw.get("tx_reported_at", ""),
                }
                devices.append(device)

            _LOGGER.debug("Fetched %d PTLevel devices", len(devices))
            return {"devices": devices}

        except aiohttp.ClientError as err:
            raise PTDevicesError(f"Connection error: {err}") from err

    async def close(self):
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()

    @staticmethod
    def _extract_csrf(html: str) -> str | None:
        """Extract CSRF token from a PTDevices HTML page."""
        match = re.search(r'name="_token"\s+value="([^"]+)"', html)
        if match:
            return match.group(1)
        match = re.search(r"\bcsrf[_-]?token['\"]?\s*[:=]\s*['\"]([^'\"]+)", html, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _extract_sensor(sensor_data: list, key: str) -> float | None:
        """Extract a sensor value by key from sensor_data array."""
        for entry in sensor_data:
            if isinstance(entry, dict) and key in entry:
                try:
                    return float(entry[key])
                except (TypeError, ValueError):
                    return None
        return None


class PTDevicesError(Exception):
    """General PTDevices API error."""


class PTDevicesAuthError(PTDevicesError):
    """Authentication error."""
