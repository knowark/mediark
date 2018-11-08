from .config import Config


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True,
            'acesslog': '-',
            'loglevel': 'debug'
        })
        self['default_factory'] = 'MemoryFactory'
        self['providers'] = PROVIDERS


PROVIDERS = {
    "ExpressionParser": {
        "method": "expression_parser"
    },
    "IdService": {
        "method": "standard_id_service"
    },
    "ImageRepository": {
        "method": "memory_image_repository",
    },
    "ImageStorageCoordinator": {
        "method": "image_storage_coordinator",
    },
    "MediarkRepository": {
        "method": "memory_mediark_repository",
    }
}
