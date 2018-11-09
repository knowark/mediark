from pathlib import Path
from ...infrastructure.data import (
    DirectoryImageFileStoreService, DirectoryAudioFileStoreService)
from .shelve_factory import ShelveFactory
from ..config import Config


class DirectoryFactory(ShelveFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def directory_image_file_store_service(self) -> (
            DirectoryImageFileStoreService):
        directory = self.config['images']['media']
        extension = self.config['images']['extension']
        return DirectoryImageFileStoreService(directory, extension)

    def directory_audio_file_store_service(self) -> (
            DirectoryAudioFileStoreService):
        directory = self.config['audios']['media']
        extension = self.config['audios']['extension']
        return DirectoryAudioFileStoreService(directory, extension)
