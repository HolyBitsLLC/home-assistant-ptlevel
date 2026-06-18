# PTLevel Home Assistant Integration

Custom integration for [PTLevel](https://paremtech.com/wireless-ptlevel/) wireless liquid level monitors by ParemTech.

> **Status:** Initial scaffolding. The PTDevices cloud API needs to be reverse-engineered to complete the integration.

## Features

- Monitor tank level percentage and estimated volume
- Battery and signal strength sensors
- Configurable polling interval
- Config Flow (UI-based setup)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant.
2. Go to **Integrations** > **Custom repositories**.
3. Add `https://github.com/YOUR_ORG/home-assistant-ptlevel` as an **Integration**.
4. Install **PTLevel**.
5. Restart Home Assistant.
6. Go to **Settings** > **Devices & Services** > **Add Integration** and search for **PTLevel**.

### Manual

1. Copy the `custom_components/ptlevel` folder into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Add the integration via the UI.

## Configuration

You will need your **PTDevices account username and password** (same as the mobile app / https://ptdevices.com).

## Reverse Engineering the API

The PTDevices cloud API is not publicly documented. To make this integration functional, you need to capture the actual API endpoints:

1. Log into [https://ptdevices.com](https://ptdevices.com) using a desktop browser (Chrome/Edge/Firefox).
2. Open **Developer Tools** (F12) and switch to the **Network** tab.
3. Look for **XHR/Fetch** requests that return JSON data.
4. Common patterns to look for:
   - `POST /api/login` or `POST /api/auth`
   - `GET /api/devices`
   - `GET /api/tanks`
   - `GET /dashboard/data`
5. Note the request URL, headers (especially `Authorization` or session cookies), and response JSON structure.
6. Update `custom_components/ptlevel/api.py` with the real endpoints and authentication flow.
7. Open a PR or issue to share your findings!

## Home Energy Management

Water tank **level** (percentage/volume) is a **state** measurement, not a **consumption** measurement. Home Assistant's Energy dashboard tracks **utility consumption** (water usage over time). If you have a flow meter or the PTLevel can estimate usage, you may be able to add it as a **water source** in the Energy dashboard.

For now, this integration exposes tank level as regular sensors for automations and dashboards.

## Missing Energy Dashboard?

If your Home Assistant **Energy** panel is missing:

1. Ensure you are logged in as an **Owner/Admin** user.
2. Check that `default_config:` is present in your `configuration.yaml`.
3. Add `energy:` to your `configuration.yaml` if missing:
   ```yaml
   energy:
   ```
4. Restart Home Assistant.
5. Clear your browser cache or try a different browser.
6. Navigate directly to `http://YOUR_HA_IP:8123/config/energy`.
7. If using a non-admin account, create a new admin user to verify.

## Integrating Enphase, Lumin, Moen, and Rheem

### Enphase (Solar)
- Home Assistant has an official **Enphase Envoy** integration.
- Go to **Settings > Devices & Services > Add Integration** and search for **Enphase Envoy**.
- It will automatically discover your Envoy gateway on the local network.
- Once added, go to **Settings > Dashboards > Energy** and add your solar production under **Solar Panels**.

### Lumin Smart Panel
- Lumin does not have an official HA integration.
- Options:
  - Use the unofficial [lumin-home-assistant](https://github.com/) integration if available, or build one using their API.
  - Use MQTT or local polling if the Lumin panel exposes data locally.
- Add individual device sensors under **Energy > Individual Devices**.

### Moen Smart Water (Flo by Moen)
- Home Assistant has a **Flo** integration for Moen smart water valves.
- Go to **Settings > Devices & Services > Add Integration** and search for **Flo**.
- This provides flow rate and water consumption.
- In the Energy dashboard, add a **Water Source** and select the Flo consumption sensor.

### Rheem/EcoNet Smart Water Heater
- Home Assistant has an **EcoNet** integration.
- Go to **Settings > Devices & Services > Add Integration** and search for **EcoNet**.
- It exposes energy usage sensors that can be added to the Energy dashboard under **Individual Devices**.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Update `api.py` once the real PTDevices API is known.
4. Submit a PR.

## License

MIT
