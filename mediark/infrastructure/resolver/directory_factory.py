from pathlib import Path
from ...infrastructure.data import DirectoryImageFileStoreService
from .shelve_factory import ShelveFactory
from ..config import Config


class DirectoryFactory(ShelveFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.home = str(Path.home())

    def directory_image_file_store_service(self) -> (
            DirectoryImageFileStoreService):
        base_path = self.home + '/media/images'
        extension = 'jpg'
        return DirectoryImageFileStoreService(base_path, extension)
