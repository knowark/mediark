from pathlib import Path
from abc import ABC, abstractmethod


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['home'] = str(Path.home())
        self['domain'] = 'http://0.0.0.0:8080'
        self['environment'] = {
            'media': self['home'] + '/media',
            'shelve': self['home'] + '/shelve',
        }
        self['download'] = self['domain'] + '/download'
        self['flask'] = {
            'USE_X_SENDFILE': False
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['images'] = {
            'media': self['environment']['media'] + '/images',
            'download': self['download'] + '/images',
            'shelve':  self['environment']['shelve'] + '/images.db',
            'extension': 'jpg'
        }
        self['audios'] = {
            'media': self['environment']['media'] + '/audios',
            'download': self['download'] + '/audios',
            'shelve':  self['environment']['shelve'] + '/audios.db',
            'extension': 'mp4'
        }
        self['providers'] = []
