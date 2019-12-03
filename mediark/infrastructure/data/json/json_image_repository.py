from ....application.models import Image
from ....application.utilities import (
    QueryParser, TenantProvider, AuthProvider)
from ....application.repositories import Repository, ImageRepository
from .json_repository import JsonRepository


class JsonImageRepository(
        JsonRepository[Image], ImageRepository):
    """Json Image Repository"""

    def __init__(self,  parser: QueryParser,
                 tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 collection_name: str = 'images') -> None:
        super().__init__(parser, tenant_provider, auth_provider,
                         collection_name, Image)
