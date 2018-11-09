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
        self['factory'] = 'MemoryFactory'

        self['providers'] = {
            "ExpressionParser": {
                "method": "expression_parser"
            },
            "IdService": {
                "method": "standard_id_service"
            },
            "ImageFileStoreService": {
                "method": "memory_image_file_store_service"
            },
            "ImageRepository": {
                "method": "memory_image_repository",
            },
            "ImageStorageCoordinator": {
                "method": "image_storage_coordinator",
            },
            "MediarkReporter": {
                "method": "memory_mediark_reporter",
            }
        }
