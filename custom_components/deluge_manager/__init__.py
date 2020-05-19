import logging
from .const import DOMAIN
from deluge_client import DelugeRPCClient
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

CONF_DELUGE_URL = "deluge_url"
deluge_url = "127.0.0.1"

CONF_DELUGE_PORT = "deluge_port"
deluge_port = ""

CONF_DELUGE_USERNAME = "deluge_username"
deluge_username = ""

CONF_DELUGE_PASSWORD = "deluge_password"
deluge_password = ""

def setup(hass, config):

    conf = config[DOMAIN]
    
    if conf[CONF_DELUGE_URL] is not None:
        deluge_url = conf[CONF_DELUGE_URL]
    
    if conf[CONF_DELUGE_PORT] is not None:
        deluge_port = conf[CONF_DELUGE_PORT]

    if conf[CONF_DELUGE_USERNAME] is not None:
        deluge_username = conf[CONF_DELUGE_USERNAME]

    if conf[CONF_DELUGE_PASSWORD] is not None:
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
