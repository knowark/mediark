from pathlib import Path
from abc import ABC, abstractmethod


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['domain'] = 'http://0.0.0.0:8080'
        self['media'] = str(Path.home().joinpath('media'))
        self['shelve'] = str(Path.home().joinpath('shelve'))
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }
        self['flask'] = {}
        self['images'] = {
            'media': '/images',
            'shelve': '/images.db',
            'extension': 'jpg'
        }
        self['audios'] = {
            'media': '/audios',
            'shelve':  '/audios.db',
            'extension': 'mp4'
        }
        self['providers'] = []
