from .repository import Repository
from .memory_repository import MemoryRepository


class MediaRepository(Repository):
    """Media Repository"""


class MemoryMediaRepository(MemoryRepository, MediaRepository):
    """Memory Media Repository"""
