from __future__ import annotations

from datetime import timedelta
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import DOMAIN, HomeAssistant
from .const import CONF_POLLING_INTERVAL, DOMAIN, CONF_PLATFORM, CONF_PROFILE, POLLING_INTERVAL, PULL_TIMEOUT, CONF_USERNAME, CONF_PASSWORD
from .lib import Platform, Title, Mode, Login

import async_timeout

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    profile = entry.data.get(CONF_PROFILE)
    platform = Platform(entry.data.get(CONF_PLATFORM))
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    sensors = []

    async def async_update_data():
        with async_timeout.timeout(PULL_TIMEOUT):
            try:
                client = await Login(username, password)
                results = await client.SearchPlayers(platform, profile, limit=1)
                me = results[0]
                profileResults = await me.profile(Title.ModernWarfare, Mode.Warzone)
                finalResults = profileResults["lifetime"]["mode"]["br"]["properties"]
                finalResults["level"] = profileResults["level"]
                return finalResults
            except Exception as exception:
                _LOGGER.error("Failed to update warzone", exc_info=1)
                raise UpdateFailed(exception)

    polling = entry.options.get(CONF_POLLING_INTERVAL, POLLING_INTERVAL)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(minutes=polling),
    )

    await coordinator.async_config_entry_first_refresh()

    for idx, ent in enumerate(coordinator.data):
        sensors.append(
            WarzoneSensor(coordinator, ent, profile)
        )
    async_add_entities(sensors, True)


class WarzoneSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, sensor, profile):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = sensor
        self._profile = profile

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._profile + "_" + DOMAIN + "_" + self._sensor

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._sensor]