from __future__ import annotations

from datetime import timedelta
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import DOMAIN, HomeAssistant
from homeassistant.exceptions import PlatformNotReady
from .const import CLIENT, DOMAIN, CONF_PLATFORM, CONF_PROFILE, POLLING_INTERVAL
from .lib import Platform, Title, Mode

import async_timeout

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=300)
PARALLEL_UPDATES = 4

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    client = hass.data[DOMAIN][entry.entry_id][CLIENT]
    profile = entry.data.get(CONF_PROFILE)
    platform = Platform(entry.data.get(CONF_PLATFORM))
    sensors = []

    async def async_update_data():
        with async_timeout.timeout(20):
            results = await client.SearchPlayers(platform, profile, limit=1)
            me = results[0]
            profileResults = await me.profile(Title.ModernWarfare, Mode.Warzone)
            finalResults = profileResults["lifetime"]["mode"]["br"]["properties"]
            finalResults["level"] = profileResults["level"]
            return finalResults

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=POLLING_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    for idx, ent in enumerate(coordinator.data):
        sensors.append(
            WarzoneSensor(coordinator, ent, coordinator.data[ent])
        )
    async_add_entities(sensors, True)


class WarzoneSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, name, state):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._state = state
        self._name = DOMAIN + "_" + name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state