from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from .config import Config
from pathlib import Path
from .development_config import DevelopmentConfig


class TrialConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'TEST'
        self['factory'] = 'CheckFactory'

        self['strategy'].update({
            "TenantSupplier": {
                "method": "check_tenant_supplier"
            },
            "ImageRepository": {
                "method": "check_image_repository",
            },
            "AudioRepository": {
                "method": "check_audio_repository",
            }
        })
