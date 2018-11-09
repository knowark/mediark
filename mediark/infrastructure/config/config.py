from pathlib import Path
from abc import ABC, abstractmethod


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['home'] = str(Path.home())
        self['environment'] = {
            'media': self['home'] + '/media',
            'shelve': self['home'] + '/shelve'
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['images'] = {
            'media': self['environment']['media'] + '/images',
            'shelve':  self['environment']['shelve'] + '/images.db',
            'extension': 'jpg'
        }
        self['providers'] = []
