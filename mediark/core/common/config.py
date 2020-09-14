import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]

config: Config = {
    'port': int(os.environ.get('MEDIARK_PORT', 6291)),
    'auto': bool(os.environ.get('MEDIARK_AUTO', True)),
    'factory': os.environ.get('MEDIARK_FACTORY', 'SqlFactory'),
    'strategies': os.environ.get(
        'MEDIARK_STRATEGIES', 'base,sql').split(','),
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


# from collections import defaultdict
# from typing import Dict, Any
# from abc import ABC, abstractmethod
# from json import loads, JSONDecodeError
# from pathlib import Path


# class Config(defaultdict, ABC):

#     @abstractmethod
#     def __init__(self):
#         self['mode'] = 'BASE'
#         self['factory'] = 'CloudFactory'
#         self['port'] = 8080
#         self['aiohttp'] = {
#             'client_max_size': 10 * 1024**2
#         }
#         self['strategies'] = ['base']
#         self['strategy'] = {}
#         self['tenancy'] = {
#             'json': Path.home() / 'tenants.json'
#         }
#         self['database'] = {}
#         self["zones"] = {
#             "default": {
#                 "dsn": 'dummy_connection://database'
#             }
#         }
#         self['environment'] = {'home': '/opt/mediark'}
#         self['domain'] = 'https://mediark.dev.nubark.cloud'
#         self['data'] = {
#             'dir_path': Path.home() / 'data',
#             'media': {
#                 'dir_path': 'media',
#                 'audios': {
#                     'dir_path': 'audios',
#                     'extension': 'webm'
#                 },
#                 'images': {
#                     'dir_path': './images',
#                     'extension': 'jpg'
#                 },
#             },
#             'shelve':  {
#                 'dir_path': 'shelve',
#                 'audios': {
#                     'dir_path': 'audios',
#                     'database': 'audios.db'
#                 },
#                 'images': {
#                     'dir_path': 'images',
#                     'database': 'images.db'
#                 },
#             },
#             'json':  {
#                 'dir_path': 'json',
#                 'audios': {
#                     'dir_path': 'audios',
#                     'database': 'audios.json'
#                 },
#                 'images': {
#                     'dir_path': 'images',
#                     'database': 'images.json'
#                 },
#             },
#             'cloud': {
#                 "swift": {
#                     "auth_url": "https://auth.cloud.ovh.net/v3/auth/tokens",
#                     "object_store_url": "",
#                     "username": "",
#                     "password": "",
#                     "container_prefix": "",
#                     "container_suffix": "dev"
#                 }
#             }
#         }


# class DevelopmentConfig(Config):
#     def __init__(self):
#         super().__init__()
#         self['mode'] = 'DEV'
#         self['factory'] = 'CheckFactory'
#         self['strategies'].extend(['http', 'check'])


# class ProductionConfig(Config):
#     def __init__(self):
#         super().__init__()
#         self['mode'] = 'PROD'
#         self['factory'] = 'CloudFactory'
#         self['strategies'].extend(['http', 'sql', 'swift'])
#         self['tenancy'] = {
#             "dsn": (
#                 "postgresql://mediark:mediark"
#                 "@localhost/mediark")
#         }
#         self["zones"] = {
#             "default": {
#                 "dsn": ("postgresql://mediark:mediark"
#                         "@localhost/mediark")
#             }
#         }
