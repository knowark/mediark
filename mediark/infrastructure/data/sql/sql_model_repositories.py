from filtrark.sql_parser import SqlParser
from ....application.models import Audio, Image
from ....application.repositories import AudioRepository, ImageRepository
from ....application.utilities import TenantProvider, AuthProvider
from .connection import ConnectionManager
from .sql_repository import SqlRepository


class SqlAudioRepository(SqlRepository, AudioRepository):
    """Sql Audio Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: ConnectionManager,
                 parser: SqlParser) -> None:
        super().__init__('audios', Audio, tenant_provider,
                         auth_provider, connection_manager, parser)


class SqlImageRepository(SqlRepository, ImageRepository):
    """Sql Image Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: ConnectionManager,
                 parser: SqlParser) -> None:
        super().__init__('images', Image, tenant_provider,
                         auth_provider, connection_manager, parser)
