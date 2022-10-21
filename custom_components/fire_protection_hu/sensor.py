import asyncio
import json
import logging
import re
import voluptuous as vol
import aiohttp
from datetime import datetime
from datetime import timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = [ ]

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "Data provided by nebih.gov.hu"
CONF_COUNTY = 'county_id'
CONF_NAME = 'name'

DEFAULT_COUNTY = ''
DEFAULT_ICON = 'mdi:fire'
DEFAULT_NAME = 'Fire Protection HU'
DEFAULT_REGION = '20'

SCAN_INTERVAL = timedelta(minutes=60)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_COUNTY, default=DEFAULT_COUNTY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    county_id = config.get(CONF_COUNTY)
    if int(county_id) > 20 or int(county_id) < 0:
      county_id = 0

    async_add_devices(
        [FireProtectionHUSensor(hass, name, county_id )],update_before_add=True)

async def async_get_fdata(self):
    fireprotection = [None] * 20
    megye = "MEGYE_KOD_"
    tuzve = "NAPI_TUZVE"

    url = 'https://tuzgyujtasitilalom.nebih.gov.hu/geoserver/nebih/wms?service=WMS&version=1.1.0&request=GetMap&layers=nebih:tuzgyujtas&styles=&bbox=384000.0,32000.0,960000.0,384000.0&width=768&height=469&srs=EPSG:23700&format=application%2Frss%2Bxml'
    async with self._session.get(url) as response:
        rsp = await response.text()

    for line in rsp.split("\n"):
      if megye in line:
        rcode = int(line.replace("<li><strong><span class=\"atr-name\">MEGYE_KOD_</span>:</strong> <span class=\"atr-value\">","") \
               .replace("</span></li>",""))
      if tuzve in line:
        if rcode != 0:
          fireprotection[rcode - 1] = int(line.replace("<li><strong><span class=\"atr-name\">NAPI_TUZVE</span>:</strong> <span class=\"atr-value\">","") \
                                  .replace("</span></li>",""))
          rcode = 0
    _LOGGER.debug(fireprotection)
    return fireprotection

class FireProtectionHUSensor(Entity):

    def __init__(self, hass, name, county_id):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._county_id = county_id
        self._state = None
        self._fdata = [None] * 20
        self._icon = DEFAULT_ICON
        self._session = async_get_clientsession(hass)

    @property
    def extra_state_attributes(self):
        attr = {}
        attr["provider"] = CONF_ATTRIBUTION
        attr["county_id"] = int(self._county_id)
        attr["data"] = self._fdata
        return attr

    @asyncio.coroutine
    async def async_update(self):

        self._fdata = await async_get_fdata(self)
        _LOGGER.debug("county_id: " + self._county_id)

        self._state = self._fdata[int(self._county_id) - 1]
        if self._state is not None and int(self._state) > 0:
          self._icon = "mdi:fire-alert"
        else:
          self._icon = "mdi:fire"

        return self._state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon
