from ..models import Audio
from .repository.repository import Repository
from .repository.memory_repository import MemoryRepository


class AudioRepository(Repository[Audio]):
    """Audio Repository"""


class MemoryAudioRepository(MemoryRepository[Audio], AudioRepository):
    """Memory Audio Repository"""
