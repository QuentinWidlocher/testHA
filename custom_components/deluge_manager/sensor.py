from homeassistant.helpers.entity import Entity
from deluge_client.client import DelugeRPCClient
from .__init__ import connect, auth, client
from datetime import timedelta
from .const import TORRENT_INFO_KEYS

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # One class instance for each torrent state
    add_entities([new_class(state)() for state in torrent_state_to_create])

SCAN_INTERVAL = timedelta(seconds=5)

torrent_state_to_create = [
    "Seeding",
    "Downloading"
    "Active",
    "Inactive"
]

# Generate a new class from BaseTorrentSensor, with state param
def new_class(state):
    return type(f"Torrents{state}", (BaseTorrentSensor,), {
        "_name": f"{state} Torrents",
        "update": lambda self: update(self, state)
    })

def update(self, state):

    global client
    global auth

    if client is None or auth is None:
        return

    if not client.connected:
        client = connect(auth)

    if not client.connected:
        return

    torrents = client.core.get_torrents_status(
        {'state': state}, ['name'])

    self._state = len(torrents.values())

class BaseTorrentSensor(Entity):

    _name = ""

    def __init__(self, name):
        """Initialize the sensor."""
        self._state = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
