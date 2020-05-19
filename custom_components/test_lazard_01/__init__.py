from .const import DOMAIN

def setup(hass, config):

    def handle_get_torrents(call):
        """Handle the service call."""
        test = call.data.get("test", "")

        hass.states.set("test_lazard_01.hello", test)

    hass.services.register(DOMAIN, "get_torrents", handle_get_torrents)

    return True
