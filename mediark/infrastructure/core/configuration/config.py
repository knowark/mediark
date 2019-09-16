from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path


class Config(defaultdict, ABC):

    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['flask'] = {}
        self['database'] = {}
        self['tenancy'] = {
            'json': Path.home() / 'tenants.json'
        }
        self['secrets'] = {}
        self['strategy'] = {}
        self['environment'] = {
            'home': '/opt/mediark'
        }
        self['data'] = {
            'dir_path': str(Path.home() / 'data'),
            'media': {
                'dir_path': './media',
                'audios': {
                    'dir_path': './audios',
                    'extension': 'webm'
                },
                'images': {
                    'dir_path': './images',
                    'extension': 'jpg'
                },
            },
            'shelve':  {
                'dir_path': './shelve',
                'audios': {
                    'dir_path': './audios',
                    'database': 'audios.db'
                },
                'images': {
                    'dir_path': './images',
                    'database': 'images.db'
                },
            }
        }
        self['media'] = str(Path('/opt/mediark/data/origin/media'))
        self['shelve'] = str(Path('/opt/mediark/data/origin/shelve'))
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
        }

        self['images'] = {
            'media': '/images',
            'shelve': '/images.db',
            'extension': 'jpg'
        }

        self['audios'] = {
            'media': '/audios',
            'shelve':  '/audios.db',
            'extension': 'webm'
        }
