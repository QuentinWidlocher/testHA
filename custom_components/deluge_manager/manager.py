from .const import DOMAIN, CONF_DELUGE_URL, CONF_DELUGE_PORT, CONF_DELUGE_USERNAME, CONF_DELUGE_PASSWORD, DEFAULTS
from deluge_client.client import DelugeRPCClient

def connect(auth):
    client = DelugeRPCClient(auth[CONF_DELUGE_URL], auth[CONF_DELUGE_PORT],
                             auth[CONF_DELUGE_USERNAME], auth[CONF_DELUGE_PASSWORD])

    client.connect()
    return client

def setup_auth(conf, params = {}, defaults = DEFAULTS):
    return {
        CONF_DELUGE_URL: get_value_in_lists(CONF_DELUGE_URL, [conf, params, defaults]),
        CONF_DELUGE_PORT: get_value_in_lists(CONF_DELUGE_PORT, [conf, params, defaults]),
        CONF_DELUGE_USERNAME: get_value_in_lists(CONF_DELUGE_USERNAME, [conf, params, defaults]),
        CONF_DELUGE_PASSWORD: get_value_in_lists(CONF_DELUGE_PASSWORD, [conf, params, defaults]),
    }

def get_value_in_lists(key, dict_list):

    for dict in dict_list:
        if key in dict:
            return dict.get(key)
    
    return None
