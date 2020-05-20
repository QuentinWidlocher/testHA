from homeassistant.helpers.entity import Entity
from deluge_client.client import DelugeRPCClient
from .__init__ import connect, auth, client
from datetime import timedelta
from .const import TORRENT_INFO_KEYS

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([TorrentList()])

SCAN_INTERVAL = timedelta(seconds=5)

class TorrentList(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Torrent List'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        global client
        global auth

        if client is None or auth is None:
            return

        if not client.connected:
            client = connect(auth)

        if not client.connected:
            return
                
        torrents = client.core.get_torrents_status({}, TORRENT_INFO_KEYS)
            
        self._state = torrents.values()
