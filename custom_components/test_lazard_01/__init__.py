from .const import DOMAIN

def setup(hass, config):
    
    def handle_hello(call):
        """Handle the service call."""
        name = call.data.get("name", "World")

        hass.states.set("test_lazard_01.hello", name)

    hass.services.register(DOMAIN, "hello", handle_hello)

    return True
