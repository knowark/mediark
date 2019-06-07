import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path



class Config(defaultdict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['environment'] = {
            'home': '/opt/mediark'
        }
        self['media'] = str(Path('/var/opt/mediark/data/templates/media'))
        self['shelve'] = str(Path('/var/opt/mediark/data/templates/shelve'))
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['flask'] = {}
        self['database'] = {}
        self['tenancy'] = {
            'json': Path.home() / 'tenants.json'
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
        self['secrets'] = {}
        self['strategy'] = {}
