from ..models import Image
from .repository.repository import Repository
from .repository.memory_repository import MemoryRepository


class ImageRepository(Repository[Image]):
    """Image Repository"""


class MemoryImageRepository(MemoryRepository[Image], ImageRepository):
    """Memory Image Repository"""
