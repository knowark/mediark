from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path


class Config(defaultdict, ABC):

    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['database'] = {}
        self['tenancy'] = {
            'json': Path.home() / 'tenants.json'
        }
        self['port'] = 8080
        self['secrets'] = {}
        self['strategy'] = {}
        self['environment'] = {
            'home': '/opt/mediark'
        }
        self['domain'] = 'https://mediark.dev.nubark.cloud'
        self['data'] = {
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
            }
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
        }
