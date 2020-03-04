from ..models import Image
from typing import List, Optional
from ..repositories import ImageRepository
from ..services import IdService, FileStoreService
from ..utilities import EntityNotFoundError
from .types import ImageDict


class ImageStorageCoordinator:
    def __init__(self, image_repository: ImageRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.image_repository = image_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def store(self, image_dict: ImageDict) -> None:
        content = image_dict.pop('data', None)
        if not content:
            raise ValueError("The image must have content.")

        image_dict.setdefault('id', self.id_service.generate_id())
        image = Image(**image_dict)
        context = vars(image)
        # uri = await self.file_store_service.store(content, context)
        uri = ''

        image.uri = uri

        await self.image_repository.add(image)

        # try:
        #     await self.image_repository.get(image.id)
        #     result = await self.image_repository.update(image)
        # except EntityNotFoundError:
        #     result = await self.image_repository.add(image)
