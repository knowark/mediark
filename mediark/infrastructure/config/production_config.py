from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True,
            'acesslog': '-',
            'loglevel': 'debug'
        })
        self['factory'] = 'ShelveFactory'

        self['providers'].update({
            "ImageRepository": {
                "method": "shelve_image_repository",
            }
        })
