DOMAIN = "deluge_manager"

CONF_DELUGE_URL = "url"
CONF_DELUGE_PORT = "port"
CONF_DELUGE_USERNAME = "username"
CONF_DELUGE_PASSWORD = "password"

DEFAULTS = {
    CONF_DELUGE_URL: "127.0.0.1",
    CONF_DELUGE_PORT: 58846,
    CONF_DELUGE_USERNAME: "deluge",
    CONF_DELUGE_PASSWORD: "deluge",
}

TORRENT_INFO_KEYS = [
    'name',
    'eta',  # en secondes
    'ratio',
    'is_finished',
    'paused',
    'state',  # Seeding, Downloading, Queued
    'progress',
]
