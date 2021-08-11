import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('MEDIARK_PORT', 8080)),
    'auto': bool(os.environ.get('MEDIARK_AUTO', True)),
    'factory': os.environ.get('MEDIARK_FACTORY', 'CloudFactory'),
    'strategies': os.environ.get(
        'MEDIARK_STRATEGIES', 'base,http,directory,sql,swift').split(','),
    'tenancy': {
        "dsn": os.environ.get('MEDIARK_TENANCY_DSN', (
            "postgresql://mediark:mediark@localhost/mediark"))
    },
    'zones': {
        "default": {
            "dsn": os.environ.get('MEDIARK_ZONES_DEFAULT_DSN', (
                "postgresql://mediark:mediark@localhost/mediark"))
        }
    },
   'secrets': {
        'tokens': os.environ.get('MEDIARK_TOKENS_SECRET', '')
    },
    'domain': os.environ.get(
        'MEDIARK_DOMAIN', "https://mediark.dev.nubark.cloud"),
    "dir_path": str(Path.home() / "data"),
    "media": {
            "dir_path": "media",
            "audios": {
                "dir_path": "audios",
            },
            "images": {
                "dir_path": "images",
            }
    },
    "shelve": {
            "dir_path": "shelve",
            "audios": {
                "dir_path": "audios",
                "database": "audios.db"
            },
            "images": {
                "dir_path": "images",
                "database": "images.db"
            }
    },
    "json": {
            "dir_path": "json",
            "audios": {
                "dir_path": "audios",
                "database": "audios.json"
            },
            "images": {
                "dir_path": "images",
                "database": "images.json"
            }
    },
    "cloud": {
            "swift": {
                "auth_url":  "https://auth.cloud.ovh.net/v3/auth/tokens",
                "object_store_url": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_OBJECT_STORE_URL',
                    ("https://storage.bhs.cloud.ovh.net/v1/"
                     "AUTH_e737167b6b424d92ae257f2d94bc1b83")),
                "username": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_USER_NAME', ""),
                "password": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_PASSWORD', ""),
                "container_prefix": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_CONTAINER_PREFIX', ""),
                "container_suffix": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_CONTAINER_SUFFIX', "main"),
            }
    },
    'environment': {
        'home': '/opt/mediark'
    },
    'aiohttp': {
        'client_max_size': 10 * 1024**2
    },
}
print(config)
