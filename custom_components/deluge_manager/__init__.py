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

    global config

    config = conf[DOMAIN]

    hass.services.register(DOMAIN, "get_torrents", lambda call: handle_get_torrents(hass, call))
    hass.services.register(DOMAIN, "connect", lambda call: handle_connect(hass, call))

    return True

def handle_connect(hass, call):
    _LOGGER.debug("handle_connect")
    
    _LOGGER.debug(hass is None)
    _LOGGER.debug(call is None)
    global client
    global config

    conf = config

    deluge_url = get_value_or_default(CONF_DELUGE_URL, conf, call.data)
    deluge_port = get_value_or_default(CONF_DELUGE_PORT, conf, call.data)
    deluge_username = get_value_or_default(CONF_DELUGE_USERNAME, conf, call.data)
    deluge_password = get_value_or_default(CONF_DELUGE_PASSWORD, conf, call.data)

    client = DelugeRPCClient(deluge_url, deluge_port, deluge_username, deluge_password)

    try:
        client.connect()
    except ConnectionRefusedError:
        _LOGGER.error("Connection to Deluge Daemon failed")
    raise PlatformNotReady

def handle_get_torrents(hass, all):
    _LOGGER.debug(f"Getting deluge status...")
    torrents = client.core.get_torrents_status({}, ['name'])
    names = []

    for id, torrent in torrents.items():
        _LOGGER.debug(torrent)
        names.append(torrent)

    hass.states.set(f"{DOMAIN}.torrents", names)

def get_value_or_default(key, conf, params):
    if key in params:
        return conf[key]
    elif key in conf:
        return params.get(key)
    else:
        return default_deluge_url
