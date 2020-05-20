def new_class(state):
    return type(f"Torrents{state}", (BaseTorrentSensor,), {
        "_name": f"{state} Torrents",
        "update": lambda self: update(self, state)
    })


def update(self, state):
    print(self.name, state, self._wow)

class SuperClass():
    _wow = "wow"

class BaseTorrentSensor(SuperClass):
    """Representation of a Sensor."""

    _name = ""

    def __init__(self):
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


torrent_state_to_create = [
    "Seeding",
    "Downloading",
    "Active",
    "Inactive"
]

test = new_class("Seeding")
test().update()
