from ....application.services import (
    ImageFileStoreService, AudioFileStoreService)
from .directory_file_store_service import DirectoryFileStoreService


class DirectoryImageFileStoreService(
        DirectoryFileStoreService, ImageFileStoreService):
    """ Directory Image File Store Service"""


class DirectoryAudioFileStoreService(
        DirectoryFileStoreService, AudioFileStoreService):
    """ Directory Image File Store Service"""
