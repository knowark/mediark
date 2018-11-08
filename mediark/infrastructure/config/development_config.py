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


PROVIDERS = [
    {
        "provide": "ExpressionParser",
        "method": "expression_parser"
    },
    {
        "provide": "IdService",
        "method": "standard_id_service"
    },
    {
        "provide": "ImageRepository",
        "method": "memory_image_repository",
        # "dependencies": ["ExpressionParser"]
    },
    {
        "provide": "ImageStorageCoordinator",
        "method": "image_storage_coordinator",
        # "dependencies": ["ImageRepository", "IdService"]
    },
    {
        "provide": "MediarkRepository",
        "method": "memory_mediark_repository",
        # "dependencies": ["ImageRepository"]
    }
]
