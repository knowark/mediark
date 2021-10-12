from injectark import Config
from ...application.domain.common import (
    User, Tenant, TenantProvider, StandardTenantProvider,
    AuthProvider, StandardAuthProvider)
from ...application.domain.models import Media, Email
from ...application.domain.services import (
    FileStoreService)
from ...application.domain.services.repositories import (
    MediaRepository, MemoryMediaRepository,
    EmailRepository, MemoryEmailRepository)
from ...application.general.suppliers import (
    TenantSupplier, MemoryTenantSupplier)
from .http_factory import HttpFactory


class CheckFactory(HttpFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def tenant_supplier(self) -> TenantSupplier:
        tenant_supplier = MemoryTenantSupplier()
        tenant_supplier.ensure_tenant({
            'id': '001',
            'name': 'Default',
        })
        return tenant_supplier

    def media_repository(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> MediaRepository:
        media_repository = MemoryMediaRepository(
            locator=tenant_provider, editor=auth_provider)
        media_repository.load({
            "default": {
                '1': Media(
                    **{'id': '1', 'reference': 'ref_1',
                       'uri': 'uri_1', 'path': 'path_1'}
                ),
                '2': Media(
                    **{'id': '2', 'reference': 'ref_2',
                       'uri': 'uri_2', 'path': 'path_2'}
                ),
                '3': Media(
                    **{'id': '3', 'reference': 'ref_3',
                       'uri': 'uri_3', 'path': 'path_3'}
                )
            }
        })
        return media_repository

    def email_repository(
            self, tenant_provider: TenantProvider,
            auth_provider: AuthProvider) -> EmailRepository:
        email_repository = MemoryEmailRepository(
            locator=tenant_provider, editor=auth_provider)
        email_repository.load({
            "default": {
                "E001": Email(
                    **{"id": "E001",
                       "name": "registered",
                       "template": "mail/auth/registered.html",
			"recipient": "info@example.com",
			"subject": "New Register",
			"type": "registered",
                        "context": {
                            "user_name": "Info",
                            "shop_url": "https://www.tempos.site",
                            "unsubscribe_link": "https://www.tempos.site"
                            }
                       }
                )
            }
        })
        return email_repository

    def file_store_service(
            self, tenant_provider: TenantProvider
    ) -> FileStoreService:
        file_store_service = super().file_store_service(tenant_provider)
        file_store_service.files = {
            "default": {
                "uri_1": b'BINARY_MEDIA_DATA'
            }
        }
        return file_store_service
