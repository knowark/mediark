import json
from pathlib import Path
from ....application.repositories import ImageRepository, AudioRepository
from ...http import HttpMediarkReporter
from ..configuration import Config
from ...web.middleware import Authenticate
from ....application.coordinators import SessionCoordinator
from ...core import JwtSupplier, JsonTenantSupplier
from ....application.utilities.tenancy import TenantProvider
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .directory_factory import DirectoryFactory


class HttpFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def jwt_supplier(self) -> JwtSupplier:
        secret_file = self.config.get('secrets', {}).get('jwt')
        secret = Path(secret_file).read_text().strip() \
            if secret_file else 'secret'
        return JwtSupplier(secret)

    def json_tenant_supplier(self) -> TenantSupplier:
        catalog_path = self.config['tenancy']['json']
        directory_data = self.config['data']['dir_path']
        return JsonTenantSupplier(catalog_path, directory_data)

    def http_mediark_reporter(
        self, tenant_provider: TenantProvider,
        image_repository: ImageRepository, audio_repository: AudioRepository
    ) -> HttpMediarkReporter:
        domain_file = Path(self.config.get('secrets', {}).get('domain'))
        print("DOMAIN FILE::: ", domain_file)
        domain = domain_file.read_text().strip() if domain_file.exists() else \
            'http://0.0.0.0:8080'
        shared_path = str(Path('/download/'+tenant_provider.tenant.slug))
        image_download = domain + shared_path + '/images'
        audio_download = domain + shared_path + '/audios'
        return HttpMediarkReporter(
            image_download, audio_download,
            image_repository, audio_repository)
