"""The warzone integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Cannot setup using YAML"""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up warzone from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    if not entry.update_listeners:
        entry.add_update_listener(async_reload_entry)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)