from .....application.services import (
    ImageFileStoreService, AudioFileStoreService)
from .swift_file_store_service import SwiftFileStoreService


class SwiftImageFileStoreService(
        SwiftFileStoreService, ImageFileStoreService):
    """ Swift Image File Store Service"""


class SwiftAudioFileStoreService(
        SwiftFileStoreService, AudioFileStoreService):
    """ Swift Image File Store Service"""
