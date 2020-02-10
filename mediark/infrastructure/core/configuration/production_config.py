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
            'workers': self.number_of_workers()
        })
        self['authentication'] = {
            "type": "jwt",
            "secret_file": Path.home().joinpath('sign.txt')
        }
        self['factory'] = 'HttpFactory'
        self['strategy'].update({
            "ImageRepository": {
                "method": "json_image_repository", "TenantSupplier": {
                    "method": "json_tenant_supplier"
                },
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
            },
        })

    def number_of_workers(self):
        return (multiprocessing.cpu_count() * 2) + 1
