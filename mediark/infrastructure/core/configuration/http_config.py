import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path
from .development_config import DevelopmentConfig


class HttpConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'JSON'
        self['authentication'] = {
            "type": "jwt",
            "secret_file": Path.home().joinpath('sign.txt')
        }
        self['factory'] = 'HttpFactory'
        self['strategy'].update({
            "ImageFileStoreService": {
                "method": "directory_image_file_store_service"
            },
            "AudioFileStoreService": {
                "method": "directory_audio_file_store_service"
            },
            "MediarkReporter": {
                "method": "http_mediark_reporter",
            },

            # Tenancy

            "TenantProvider": {
                "method": "standard_tenant_provider"
            },

            "TenantSupplier": {
                "method": "json_tenant_supplier"
            }
        })
