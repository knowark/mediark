from abc import ABC, abstractmethod


class Config(dict, ABC):
    @abstractmethod
    def __init__(self):
        self['mode'] = 'BASE'
        self['environment'] = {
            'home': '/opt/mediark'
        }
        self['gunicorn'] = {
            'bind': '%s:%s' % ('0.0.0.0', '8080'),
            'workers': 1,
            'worker_class': 'gevent',
            'debug': False
        }


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True
        })
