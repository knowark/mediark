from ....application.models import Image, Audio
from ....application.repositories import (
    Repository, ImageRepository, AudioRepository)
from .shelve_repository import ShelveRepository


class ShelveImageRepository(ShelveRepository[Image], ImageRepository):
    """Shelve Image Repository"""


class ShelveAudioRepository(ShelveRepository[Audio], AudioRepository):
    """Shelve Audio Repository"""
