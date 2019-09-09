import multiprocessing
from collections import defaultdict
from typing import Dict, Any
from abc import ABC, abstractmethod
from json import loads, JSONDecodeError
from .shelve_config import ShelveConfig
from pathlib import Path


class DirectoryConfig(ShelveConfig):
    def __init__(self):
        super().__init__()
        self['factory'] = 'DirectoryFactory'
