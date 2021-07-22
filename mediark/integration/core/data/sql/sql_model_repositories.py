from filtrark.sql_parser import SqlParser
from modelark import SqlRepository
from .....application.domain.models import Media
from .....application.domain.repositories import MediaRepository
from .....application.domain.common import TenantProvider, AuthProvider
from .connection import ConnectionManager


class SqlMediaRepository(SqlRepository, MediaRepository):
    """Sql Audio Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: ConnectionManager,
                 parser: SqlParser) -> None:
        super().__init__('media', Media, connection_manager,
                         parser, tenant_provider, auth_provider)
