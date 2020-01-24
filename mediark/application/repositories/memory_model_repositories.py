from .repository import Repository
from .memory_repository import MemoryRepository


class AudioRepository(Repository):
    """Audio Repository"""


class ImageRepository(Repository):
    """Image Repository"""


class MemoryAudioRepository(MemoryRepository, AudioRepository):
    """Memory Audio Repository"""


class MemoryImageRepository(MemoryRepository, ImageRepository):
    """Memory Image Repository"""
