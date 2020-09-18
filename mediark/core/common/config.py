import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('MEDIARK_PORT', 6291)),
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
    'cloud': {
        "swift": {
            "auth_url": "https://auth.cloud.ovh.net/v3/auth/tokens",
            "object_store_url": "",
            "username": "",
            "password": "",
            "container_prefix": "",
            "container_suffix": "dev"
        }
    },
    'media': {
        'dir_path': 'media',
        'audios': {
            'dir_path': 'audios',
            'extension': 'webm'
        },
        'images': {
            'dir_path': './images',
            'extension': 'jpg'
        }
    },
    'data': {
            'dir_path': Path.home() / 'data',
            'media': {
                'dir_path': 'media',
                'audios': {
                    'dir_path': 'audios',
                    'extension': 'webm'
                },
                'images': {
                    'dir_path': './images',
                    'extension': 'jpg'
                },
            },
            'shelve':  {
                'dir_path': 'shelve',
                'audios': {
                    'dir_path': 'audios',
                    'database': 'audios.db'
                },
                'images': {
                    'dir_path': 'images',
                    'database': 'images.db'
                },
            },
            'json':  {
                'dir_path': 'json',
                'audios': {
                    'dir_path': 'audios',
                    'database': 'audios.json'
                },
                'images': {
                    'dir_path': 'images',
                    'database': 'images.json'
                },
            },
    },
    'domain': {
        'https://mediark.dev.nubark.cloud'
    },
}
