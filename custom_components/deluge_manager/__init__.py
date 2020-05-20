import logging
from .const import DOMAIN, CONF_DELUGE_URL, CONF_DELUGE_PORT, CONF_DELUGE_USERNAME, CONF_DELUGE_PASSWORD, DEFAULTS, TORRENT_INFO_KEYS
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from deluge_client import DelugeRPCClient
from homeassistant.exceptions import PlatformNotReady
from .manager import setup_auth, connect

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_DELUGE_URL, default=DEFAULTS[CONF_DELUGE_URL]): cv.string,
        vol.Optional(CONF_DELUGE_PORT, default=DEFAULTS[CONF_DELUGE_PORT]): cv.port,
        vol.Optional(CONF_DELUGE_USERNAME, default=DEFAULTS[CONF_DELUGE_USERNAME]): cv.string,
        vol.Optional(CONF_DELUGE_PASSWORD, default=DEFAULTS[CONF_DELUGE_PASSWORD]): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

client = None
auth = None

def setup(hass, conf):

    global client
    global auth

    config = conf[DOMAIN]

    auth = setup_auth(config)
    client = connect(auth)

    def handle_connect(call):
        _LOGGER.info("Connecting to Deluge...")

        global client

        auth = setup_auth(config, call.data)

        try:
            client = connect(auth)
        except ConnectionRefusedError:
            _LOGGER.error("Connection to Deluge Daemon failed")
            raise PlatformNotReady

    def handle_get_torrents(call):
        _LOGGER.info(f"Getting Deluge torrent list...")
        torrents = client.core.get_torrents_status({}, ["name"])
        names = []

        for torrent in torrents.values():
            names.append(torrent[b'name'].decode('UTF-8'))

        hass.states.set(f"{DOMAIN}.torrents", names)

    hass.services.register(DOMAIN, "get_torrents", handle_get_torrents)
    hass.services.register(DOMAIN, "connect", handle_connect)

    return True
