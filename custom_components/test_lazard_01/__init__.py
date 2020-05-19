from .const import DOMAIN

def setup(hass, config):
    hass.states.set("test_lazard_01.world", "Paulus")
    return True