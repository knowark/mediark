import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('MEDIARK_PORT') or 8080),
    'auto': bool(os.environ.get('MEDIARK_AUTO') or True),
    'factory': os.environ.get('MEDIARK_FACTORY') or 'CloudFactory',
    'strategies': os.environ.get(
        'MEDIARK_STRATEGIES') or 'base,http,directory,sql,swift'.split(','),
    'tenancy': {
        "dsn": os.environ.get('MEDIARK_TENANCY_DSN') or (
            "postgresql://mediark:mediark@localhost/mediark")
    },
    'zones': {
        "default": {
            "dsn": os.environ.get('MEDIARK_ZONES_DEFAULT_DSN') or (
                "postgresql://mediark:mediark@localhost/mediark")
        }
    },
   'secrets': {
        'tokens': os.environ.get('MEDIARK_TOKENS_SECRET') or ''
    },
    'domain': os.environ.get(
        'MEDIARK_DOMAIN') or "https://mediark.dev.nubark.cloud",
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
    "mail": {
        "sender": os.environ.get(
            'MEDIARK_MAIL_SENDER') or "",
        "host": os.environ.get(
            'MEDIARK_MAIL_HOST') or "",
        "port": int(os.environ.get(
            'MEDIARK_MAIL_PORT') or 0),
        "username": os.environ.get(
            'MEDIARK_MAIL_USERNAME') or "",
        "password": os.environ.get(
            'MEDIARK_MAIL_PASSWORD') or "",
        "path": os.environ.get(
            'MEDIARK_MAIL_PATCH') or ""
    },
    "cloud": {
            "swift": {
                "auth_url":  "https://auth.cloud.ovh.net/v3/auth/tokens",
                "object_store_url": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_OBJECT_STORE_URL') or
                    ("https://storage.bhs.cloud.ovh.net/v1/"
                     "AUTH_e737167b6b424d92ae257f2d94bc1b83"),
                "username": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_USER_NAME') or "",
                "password": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_PASSWORD') or "",
                "container_prefix": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_CONTAINER_PREFIX') or "",
                "container_suffix": os.environ.get(
                    'MEDIARK_CLOUD_SWIFT_CONTAINER_SUFFIX') or "main",
            }
    },
    'environment': {
        'home': '/opt/mediark'
    },
    'aiohttp': {
        'client_max_size': 10 * 1024**2
    },
}
def sanitize(config):
    if type(config) is dict:
        return {key: sanitize(value) for key, value in
                config.items() if value and sanitize(value)}
    return config
