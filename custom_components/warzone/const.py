"""Constants for the warzone integration."""

DOMAIN = "warzone"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_PLATFORM = "platform"
PLATFORM_TYPES = {
    "xbl": "Xbox",
    "uno": "Activision",
    "battle": "Battle.Net",
    "steam": "Steam",
    "psn": "Playstation"
}

CONF_PROFILE = "profile"

CONF_POLLING_INTERVAL = "polling"
POLLING_INTERVAL = 60
PULL_TIMEOUT = 20