from ....application.repositories import ImageRepository, AudioRepository
from ...http import HttpMediarkReporter
from ..configuration import Config
from ...web.middleware import Authenticate
from ....application.coordinators import SessionCoordinator
from ...core.crypto import JwtSupplier
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .directory_factory import DirectoryFactory


class HttpFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
    
    def middleware_authenticate(
            self, jwt_supplier: JwtSupplier,
            tenant_supplier: TenantSupplier,
            session_coordinator: SessionCoordinator) -> Authenticate:
        return Authenticate(
            jwt_supplier, tenant_supplier, session_coordinator)

    def jwt_supplier(self) -> JwtSupplier:
        secret = self.access_config['secret']
        return JwtSupplier(secret)

    def jwt_supplier(self) -> JwtSupplier:
        secret = 'secret'
        secret_file = self.config.get('secrets', {}).get('jwt')
        # if secret_file:
        #     secret = Path(secret_file).read_text().strip()
        return JwtSupplier(secret)

    def http_mediark_reporter(self, image_repository: ImageRepository,
                              audio_repository: AudioRepository
                              ) -> HttpMediarkReporter:
        image_download = self.config['domain'] + '/download/images'
        audio_download = self.config['domain'] + '/download/audios'
        return HttpMediarkReporter(
            image_download, audio_download,
            image_repository, audio_repository)
