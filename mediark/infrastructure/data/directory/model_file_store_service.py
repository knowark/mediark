from ....application.services import ImageFileStoreService
from .directory_file_store_service import DirectoryFileStoreService


class DirectoryImageFileStoreService(
        DirectoryFileStoreService, ImageFileStoreService):
    """ Directory Image File Store Service"""
