"""Config flow for warzone integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from voluptuous.schema_builder import Undefined

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from .lib import Login, Platform
from .const import CONF_POLLING_INTERVAL, DOMAIN, CONF_PASSWORD, CONF_PLATFORM, CONF_PROFILE, CONF_USERNAME, PLATFORM_TYPES, POLLING_INTERVAL

_LOGGER = logging.getLogger(__name__)

# STEP_USER_DATA_SCHEMA = vol.Schema({CONF_USER: str, CONF_PASSWORD: str, vol.Required(CONF_PLATFORM): vol.In([CONF_PLATFORM_XBOX, CONF_PLATFORM_PLAYSTATION]), CONF_PROFILE: str})
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_PLATFORM): vol.In(PLATFORM_TYPES),
    vol.Required(CONF_PROFILE): str,
})

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
    wz = Warzone(data[CONF_USERNAME], data[CONF_PASSWORD], data[CONF_PLATFORM], data[CONF_PROFILE])

    if not await wz.authenticate():
         raise InvalidAuth

    return {"title": "Warzone - " + data[CONF_PROFILE]}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for warzone."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

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



class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Yeelight."""

    def __init__(self, config_entry):
        """Initialize the option flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            options = {**self._config_entry.options}
            options.update(user_input)
            return self.async_create_entry(title="", data=options)

        polling = self._config_entry.options.get(CONF_POLLING_INTERVAL, POLLING_INTERVAL)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_POLLING_INTERVAL, default=polling, msg="message", description="description"): cv.positive_int,
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
