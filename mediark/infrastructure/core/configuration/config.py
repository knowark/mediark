import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path



class Config(defaultdict, ABC):

    def number_of_workers(self):
        return (multiprocessing.cpu_count() * 2) + 1

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
        self['media'] = str(Path('/opt/mediark/data/servagro/media'))
        self['shelve'] = str(Path('/opt/mediark/data/servagro/shelve'))
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': self.number_of_workers(),
            'worker_class': 'gevent',
            'debug': False
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
