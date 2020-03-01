import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from pathlib import Path
from .http_config import HttpConfig


class JsonConfig(HttpConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'JSON'
        self['authentication'] = {
            "type": "jwt",
            "secret_file": Path.home().joinpath('sign.txt')
        }
        self['factory'] = 'JsonFactory'
        self['strategy'].update({
            "ImageRepository": {
                "method": "json_image_repository",
            },
            "AudioRepository": {
                "method": "json_audio_repository",
            },
            "ImageFileStoreService": {
                "method": "directory_image_file_store_service"
            },
            "AudioFileStoreService": {
                "method": "directory_audio_file_store_service"
            },

            # Tenancy

            "TenantProvider": {
                "method": "standard_tenant_provider"
            },

            "TenantSupplier": {
                "method": "json_tenant_supplier"
            },
        })
