import logging
from .const import DOMAIN
from deluge_client import DelugeRPCClient
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

CONF_DELUGE_URL = "url"
deluge_url = "127.0.0.1"

CONF_DELUGE_PORT = "port"
deluge_port = "58846"

CONF_DELUGE_USERNAME = "username"
deluge_username = ""

CONF_DELUGE_PASSWORD = "password"
deluge_password = ""

def setup(hass, config):

    _LOGGER.debug(config)

    conf = config[DOMAIN]
    
    if CONF_DELUGE_URL in conf:
        deluge_url = conf[CONF_DELUGE_URL]
    
    if CONF_DELUGE_PORT in conf:
        deluge_port = conf[CONF_DELUGE_PORT]

    if CONF_DELUGE_USERNAME in conf:
        deluge_username = conf[CONF_DELUGE_USERNAME]

    if CONF_DELUGE_PASSWORD in conf:
        deluge_password = conf[CONF_DELUGE_PASSWORD]

    client = DelugeRPCClient(deluge_url, deluge_port,
                             deluge_username, deluge_password)

    try:
        client.connect()
    except ConnectionRefusedError:
        _LOGGER.error("Connection to Deluge Daemon failed")
        raise PlatformNotReady

    def handle_get_torrents(call):
        _LOGGER.debug(f"Getting deluge status on {deluge_url}")

    hass.services.register(DOMAIN, "get_torrents", handle_get_torrents)

    return True
