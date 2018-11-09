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
        download = self.config['images']['download']
        return DirectoryImageFileStoreService(directory, extension, download)

    def directory_audio_file_store_service(self) -> (
            DirectoryAudioFileStoreService):
        directory = self.config['audios']['media']
        extension = self.config['audios']['extension']
        download = self.config['audios']['download']
        return DirectoryAudioFileStoreService(directory, extension, download)
