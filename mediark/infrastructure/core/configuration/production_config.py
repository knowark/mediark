import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path
from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'PROD'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['authentication'] = {
            "type": "jwt",
            "secret_file": str(Path.home().joinpath('sign.txt'))
        }
        self['secrets'] = {
            "jwt": str(Path.home().joinpath('sign.txt'))
        }
        self['factory'] = 'HttpFactory'

        self['strategy'].update({
            "JwtSupplier": {
                "method": "jwt_supplier"
            },
            "Authenticate": {
                "method": "middleware_authenticate"
            },
            "ImageRepository": {
                "method": "shelve_image_repository",
            },
            "ImageFileStoreService": {
                "method": "directory_image_file_store_service"
            },
            "AudioRepository": {
                "method": "shelve_audio_repository",
            },
            "AudioFileStoreService": {
                "method": "directory_audio_file_store_service"
            },
            "MediarkReporter": {
                "method": "http_mediark_reporter",
            }
        })
