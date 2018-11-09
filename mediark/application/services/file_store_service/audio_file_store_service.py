from .file_store_service import FileStoreService
from .memory_file_store_service import MemoryFileStoreService


class AudioFileStoreService(FileStoreService):
    """Audio File Store Service"""


class MemoryAudioFileStoreService(
        MemoryFileStoreService, AudioFileStoreService):
    """Memory Audio File Store Service"""
