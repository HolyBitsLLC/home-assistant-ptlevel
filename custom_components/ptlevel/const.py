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
SENSOR_TANK_VOLUME = "tank_volume"
SENSOR_BATTERY = "battery"
SENSOR_SIGNAL = "signal_strength"
SENSOR_LAST_UPDATE = "last_update"

SENSOR_TYPES = {
    SENSOR_TANK_LEVEL: {
        "name": "Tank Level",
        "unit": "%",
        "device_class": None,
        "icon": "mdi:water-percent",
        "state_class": "measurement",
    },
    SENSOR_TANK_VOLUME: {
        "name": "Tank Volume",
        "unit": "L",  # or gal, configurable later
        "device_class": "volume",
        "icon": "mdi:water",
        "state_class": "measurement",
    },
    SENSOR_BATTERY: {
        "name": "Battery",
        "unit": "%",
        "device_class": "battery",
        "icon": "mdi:battery",
        "state_class": "measurement",
    },
    SENSOR_SIGNAL: {
        "name": "Signal Strength",
        "unit": "dBm",
        "device_class": "signal_strength",
        "icon": "mdi:signal",
        "state_class": "measurement",
    },
    SENSOR_LAST_UPDATE: {
        "name": "Last Update",
        "unit": None,
        "device_class": "timestamp",
        "icon": "mdi:clock-outline",
        "state_class": None,
    },
}
