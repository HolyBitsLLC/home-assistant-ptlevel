"""Constants for the PTLevel integration."""

DOMAIN = "ptlevel"

# API Configuration
DEFAULT_API_BASE = "https://ptdevices.com"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_API_BASE = "api_base"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes

# Sensor types
SENSOR_TANK_LEVEL = "tank_level"
SENSOR_TANK_LEVEL_IN = "tank_level_inches"
SENSOR_TANK_VOLUME = "tank_volume"
SENSOR_BATTERY_VOLTAGE = "battery_voltage"
SENSOR_TEMPERATURE = "temperature"
SENSOR_BATTERY_STATUS = "battery_status"
SENSOR_ONLINE = "online"
SENSOR_FIRMWARE = "firmware_version"
SENSOR_LAST_UPDATE = "last_update"

SENSOR_TYPES = {
    SENSOR_TANK_LEVEL: {
        "name": "Tank Level",
        "unit": "%",
        "device_class": None,
        "icon": "mdi:water-percent",
        "state_class": "measurement",
    },
    SENSOR_TANK_LEVEL_IN: {
        "name": "Tank Depth",
        "unit": "in",
        "device_class": "distance",
        "icon": "mdi:arrow-collapse-vertical",
        "state_class": "measurement",
    },
    SENSOR_TANK_VOLUME: {
        "name": "Tank Volume",
        "unit": "gal",
        "device_class": "volume",
        "icon": "mdi:water",
        "state_class": "measurement",
    },
    SENSOR_BATTERY_VOLTAGE: {
        "name": "Battery Voltage",
        "unit": "V",
        "device_class": "voltage",
        "icon": "mdi:battery",
        "state_class": "measurement",
    },
    SENSOR_TEMPERATURE: {
        "name": "Temperature",
        "unit": "°F",
        "device_class": "temperature",
        "icon": "mdi:thermometer",
        "state_class": "measurement",
    },
    SENSOR_BATTERY_STATUS: {
        "name": "Battery Status",
        "unit": None,
        "device_class": None,
        "icon": "mdi:battery-check",
        "state_class": None,
    },
    SENSOR_ONLINE: {
        "name": "Online",
        "unit": None,
        "device_class": "connectivity",
        "icon": "mdi:cloud-check",
        "state_class": None,
    },
    SENSOR_FIRMWARE: {
        "name": "Firmware Version",
        "unit": None,
        "device_class": None,
        "icon": "mdi:chip",
        "state_class": None,
    },
    SENSOR_LAST_UPDATE: {
        "name": "Last Update",
        "unit": None,
        "device_class": "timestamp",
        "icon": "mdi:clock-outline",
        "state_class": None,
    },
}
