from .file_store_service import FileStoreService
from .memory_file_store_service import MemoryFileStoreService


class ImageFileStoreService(FileStoreService):
    """Image File Store Service"""


class MemoryImageFileStoreService(
        MemoryFileStoreService, ImageFileStoreService):
    """Memory Image File Store Service"""
