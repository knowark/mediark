from ....application.models import Audio
from ....application.utilities import (
    QueryParser, TenantProvider, AuthProvider)
from ....application.repositories import Repository, AudioRepository
from .json_repository import JsonRepository


class JsonAudioRepository(
        JsonRepository[Audio], AudioRepository):
    """Json Audio Repository"""

    def __init__(self,  parser: QueryParser,
                 tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 collection_name: str = 'audios') -> None:
        super().__init__(parser, tenant_provider, auth_provider,
                         collection_name, Audio)
