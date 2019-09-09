import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from .development_config import DevelopmentConfig
from pathlib import Path


class ShelveConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['factory'] = 'ShelveFactory'
