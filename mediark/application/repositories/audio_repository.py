from ..models import Audio
from .repository import Repository
from .memory_repository import MemoryRepository


class AudioRepository(Repository[Audio]):
    """Audio Repository"""


class MemoryAudioRepository(MemoryRepository[Audio], AudioRepository):
    """Memory Audio Repository"""
