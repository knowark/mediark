from .shelve_config import ShelveConfig


class DirectoryConfig(ShelveConfig):
    def __init__(self):
        super().__init__()
        self['factory'] = 'DirectoryFactory'
