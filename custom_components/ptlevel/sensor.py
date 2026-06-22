"""Sensor platform for PTLevel integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    SENSOR_BATTERY_STATUS,
    SENSOR_BATTERY_VOLTAGE,
    SENSOR_FIRMWARE,
    SENSOR_LAST_UPDATE,
    SENSOR_ONLINE,
    SENSOR_TANK_LEVEL,
    SENSOR_TANK_LEVEL_IN,
    SENSOR_TANK_VOLUME,
    SENSOR_TEMPERATURE,
)
from .coordinator import PTLevelCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PTLevel sensor based on a config entry."""
    coordinator: PTLevelCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for device in coordinator.data.get("devices", []):
        for sensor_key, sensor_info in SENSOR_TYPES.items():
            entities.append(
                PTLevelSensor(
                    coordinator=coordinator,
                    device=dict(device),
                    sensor_key=sensor_key,
                    sensor_info=sensor_info,
                )
            )

    async_add_entities(entities)


class PTLevelSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PTLevel Sensor."""

    def __init__(
        self,
        coordinator: PTLevelCoordinator,
        device: dict,
        sensor_key: str,
        sensor_info: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device["id"]
        self._sensor_key = sensor_key
        self._attr_name = f"{device['name']} {sensor_info['name']}"
        self._attr_unique_id = f"{device['id']}_{sensor_key}"
        self._attr_native_unit_of_measurement = sensor_info.get("unit")
        self._attr_device_class = sensor_info.get("device_class")
        self._attr_icon = sensor_info.get("icon")
        if sensor_info.get("state_class"):
            self._attr_state_class = sensor_info["state_class"]

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device["id"])},
            name=device["name"],
            manufacturer="ParemTech",
            model="PTLevel Wireless Tank Monitor",
            sw_version=device.get("firmware_version"),
            hw_version=f"TX v{device.get('tx_version', '')}" if device.get("tx_version") else None,
            configuration_url="https://ptdevices.com",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data.get("devices", []):
            if device["id"] == self._device_id:
                if self._sensor_key == SENSOR_TANK_LEVEL:
                    return device.get("level_percent")
                elif self._sensor_key == SENSOR_TANK_LEVEL_IN:
                    return device.get("level_inches")
                elif self._sensor_key == SENSOR_TANK_VOLUME:
                    return device.get("volume")
                elif self._sensor_key == SENSOR_BATTERY_VOLTAGE:
                    return device.get("battery_voltage")
                elif self._sensor_key == SENSOR_TEMPERATURE:
                    return device.get("temperature")
                elif self._sensor_key == SENSOR_BATTERY_STATUS:
                    return "Good" if device.get("battery_ok") else "Low"
                elif self._sensor_key == SENSOR_ONLINE:
                    return "Online" if device.get("online") else "Offline"
                elif self._sensor_key == SENSOR_FIRMWARE:
                    return device.get("firmware_version")
                elif self._sensor_key == SENSOR_LAST_UPDATE:
                    return device.get("last_updated")
        return None
