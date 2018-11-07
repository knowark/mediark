from ..models import Image
from ..repositories import ImageRepository
from ..services import IdService
from .types import ImageDict


class ImageStorageCoordinator:
    def __init__(self, image_repository: ImageRepository,
                 id_service: IdService) -> None:
        self.image_repository = image_repository
        self.id_service = id_service

    def store(self, image_dict: ImageDict):
        if 'id' not in image_dict:
            image_dict['id'] = self.id_service.generate_id()

        image = Image(**image_dict)
        self.image_repository.add(image)
