from deluge_client import DelugeRPCClient

keys = [
    'name',
    'eta', # en secondes
    'ratio',
    'is_finished',
    'paused',
    'state', # Seeding, Downloading, Queued
    'progress',
]

def dprint(val):
    print(val.decode('UTF-8'))

with DelugeRPCClient("127.0.0.1", 58846, "deluge", "deluge") as client:
    if not client.connected:
        print('Unable to connect')
        exit()

    torrents = client.core.get_torrents_status({'state': 'Downloading'}, ['name'])

    print(len(torrents.keys()))
