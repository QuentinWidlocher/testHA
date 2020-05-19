import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_DELUGE_URL = "deluge_url"
deluge_url = "127.0.0.1"

def setup(hass, config):

    deluge_url = config[CONF_DELUGE_URL]

    def handle_get_torrents(call):
        _LOGGER.debug(f"Getting deluge status on {deluge_url}")

    hass.services.register(DOMAIN, "get_torrents", handle_get_torrents)

    return True
