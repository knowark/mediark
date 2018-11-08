from ....application.models import Image
from ....application.repositories import Repository, ImageRepository
from .shelve_repository import ShelveRepository


class ShelveImageRepository(ShelveRepository[Image], ImageRepository):
    """Shelve Image Repository"""
