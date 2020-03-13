from filtrark.sql_parser import SqlParser
from ....application.models import Media
from ....application.repositories import MediaRepository
from ....application.utilities import TenantProvider, AuthProvider
from .connection import ConnectionManager
from .sql_repository import SqlRepository


class SqlMediaRepository(SqlRepository, MediaRepository):
    """Sql Audio Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: ConnectionManager,
                 parser: SqlParser) -> None:
        super().__init__('media', Media, tenant_provider,
                         auth_provider, connection_manager, parser)
