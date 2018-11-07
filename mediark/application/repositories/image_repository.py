from ..models import Image
from .repository import Repository
from .memory_repository import MemoryRepository


class ImageRepository(Repository[Image]):
    """Image Repository"""


class MemoryImageRepository(MemoryRepository[Image], ImageRepository):
    """Memory Image Repository"""
