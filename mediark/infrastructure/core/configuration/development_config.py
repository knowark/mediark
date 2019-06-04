import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from .config import Config
from pathlib import Path


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True,
            'acesslog': '-',
            'loglevel': 'debug'
        })
        self['authentication'] = {
            "type": "jwt",
            "secret_file": str(Path.home().joinpath('sign.txt'))
        }
        self['secrets'] = {
            "jwt": str(Path.home().joinpath('sign.txt'))
        }
        self['factory'] = 'MemoryFactory'

        self['strategy'].update({
            "ExpressionParser": {
                "method": "expression_parser"
            },
            "TenantSupplier": {
                "method": "tenant_supplier"
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
            "AudioFileStoreService": {
                "method": "memory_audio_file_store_service"
            },
            "AudioRepository": {
                "method": "memory_audio_repository",
            },
            "AudioStorageCoordinator": {
                "method": "audio_storage_coordinator",
            },
            "MediarkReporter": {
                "method": "memory_mediark_reporter",
            }
        })
