# from abc import ABC, abstractmethod
# from .config import Config
# from ...application.repositories import (
#     ExpressionParser, MemoryImageRepository)
# from ...application.services import StandardIdService
# from ...application.coordinators import ImageStorageCoordinator
# from ...application.reporters import MemoryMediarkReporter


class Registry(dict):
    def __init__(self) -> None:
        pass


# class MemoryRegistry(Registry):

#     def __init__(self, config: Config) -> None:
#         super().__init__(config)

#         parser = ExpressionParser()
#         image_repository = MemoryImageRepository(parser)

#         id_service = StandardIdService()

#         image_storage_coordinator = ImageStorageCoordinator(
#             image_repository, id_service)

#         mediark_reporter = MemoryMediarkReporter(image_repository)

#         self['image_storage_coordinator'] = image_storage_coordinator
#         self['mediark_reporter'] = mediark_reporter
