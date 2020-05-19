import logging
from .const import DOMAIN
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from deluge_client import DelugeRPCClient
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

CONF_DELUGE_URL = "url"
default_deluge_url = "127.0.0.1"

CONF_DELUGE_PORT = "port"
default_deluge_port = 58846

CONF_DELUGE_USERNAME = "username"
default_deluge_username = "deluge"

CONF_DELUGE_PASSWORD = "password"
default_deluge_password = "deluge"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_DELUGE_URL, default=default_deluge_url): cv.string,
        vol.Optional(CONF_DELUGE_PORT, default=default_deluge_port): cv.port,
        vol.Optional(CONF_DELUGE_USERNAME, default="default_deluge_username"): cv.string,
        vol.Optional(CONF_DELUGE_PASSWORD, default="default_deluge_password"): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

client = None
config = None

def setup(hass, conf):

    global client
    global config

    config = conf[DOMAIN]

    def handle_get_torrents(call):
        _LOGGER.debug(f"Getting deluge status...")
        torrents = client.core.get_torrents_status({}, ['name'])
        for id, torrent in torrents.items():
            _LOGGER.debug(torrent['name'])

    def handle_connect():
        global client
        global config
        conf = config

        if CONF_DELUGE_URL in conf:
            deluge_url = conf[CONF_DELUGE_URL]
        else:
            deluge_url = default_deluge_url

        if CONF_DELUGE_PORT in conf:
            deluge_port = conf[CONF_DELUGE_PORT]
        else:
            deluge_port = default_deluge_port

        if CONF_DELUGE_USERNAME in conf:
            deluge_username = conf[CONF_DELUGE_USERNAME]
        else:
            deluge_username = default_deluge_username

        if CONF_DELUGE_PASSWORD in conf:
            deluge_password = conf[CONF_DELUGE_PASSWORD]
        else:
            deluge_password = default_deluge_password

        client = DelugeRPCClient(deluge_url, deluge_port,
                                deluge_username, deluge_password)

        try:
            client.connect()
        except ConnectionRefusedError:
            _LOGGER.error("Connection to Deluge Daemon failed")
            raise PlatformNotReady

    hass.services.register(DOMAIN, "get_torrents", handle_get_torrents)
    hass.services.register(DOMAIN, "connect", handle_connect)

    return True
