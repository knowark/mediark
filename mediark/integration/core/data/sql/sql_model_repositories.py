from filtrark.sql_parser import SqlParser
from modelark import SqlRepository
from .....application.domain.models import Media, Email
from .....application.domain.services.repositories import (
    MediaRepository, EmailRepository)
from .....application.domain.common import TenantProvider, AuthProvider
from .....application.general.connector import Connector


class SqlMediaRepository(SqlRepository, MediaRepository):
    """Sql Audio Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: Connector,
                 parser: SqlParser) -> None:
        super().__init__('media', Media, connection_manager,
                         parser, tenant_provider, auth_provider)


class SqlEmailRepository(SqlRepository, EmailRepository):
    """Sql Email Repository"""

    def __init__(self, tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: Connector,
                 parser: SqlParser) -> None:
        super().__init__('emails', Email, connection_manager,
                         parser, tenant_provider, auth_provider)
