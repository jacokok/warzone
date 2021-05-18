"""Config flow for warzone integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from .lib import Login
from .lib import Platform
from .const import DOMAIN, CONF_PASSWORD, CONF_PLATFORM, CONF_PROFILE, CONF_USER

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({CONF_USER: str, CONF_PASSWORD: str, CONF_PLATFORM: str, CONF_PROFILE: str})

class Warzone:

    def __init__(self, username: str, password: str, platform: str, profile: str) -> None:
        """Initialize."""
        self.username = username
        self.password = password
        self.platform = platform
        self.profile = profile

    async def authenticate(self) -> bool:
        """Test if auth is working"""
        client = await Login(self.username, self.password)
        results = await client.SearchPlayers(Platform(self.platform), self.profile, limit=1)
        if len(results) > 0:
            return True
        else:
            return False

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input"""
    wz = Warzone(data[CONF_USER], data[CONF_PASSWORD], data[CONF_PLATFORM], data[CONF_PROFILE])

    if not await wz.authenticate():
         raise InvalidAuth

    return {"title": "Warzone"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for warzone."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            data_schema = {
                vol.Required(CONF_USER, CONF_USER, CONF_USER, CONF_USER): str,
                vol.Required(CONF_PASSWORD, CONF_PASSWORD, CONF_PASSWORD, CONF_PASSWORD): str,
                vol.Required(CONF_PLATFORM, CONF_PLATFORM, "xbl", CONF_PLATFORM): str,
                vol.Required(CONF_PROFILE, CONF_PROFILE, "MajorNelson", CONF_PROFILE): str,
            }

            return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""