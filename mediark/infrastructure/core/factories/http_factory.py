import json
from pathlib import Path
from ....application.repositories import ImageRepository, AudioRepository
from ...http import HttpMediarkReporter
from ..configuration import Config
from ....application.coordinators import SessionCoordinator
from ....application.utilities.tenancy import TenantProvider
from ..tenancy import TenantSupplier, MemoryTenantSupplier
from .directory_factory import DirectoryFactory


class HttpFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def http_mediark_reporter(
        self, tenant_provider: TenantProvider,
        image_repository: ImageRepository, audio_repository: AudioRepository
    ) -> HttpMediarkReporter:
        # domain_file = Path(self.config.get('secrets', {}).get('domain'))
        # domain = domain_file.read_text().strip() if domain_file.exists() \
        #   else 'http://0.0.0.0:8080'

        # shared_path = str(Path('/download/'+tenant_provider.tenant.slug))
        # image_download = domain + shared_path + '/images'
        # audio_download = domain + shared_path + '/audios'

        # image_download = self.config['domain'] + '/download/images'
        # audio_download = self.config['domain'] + '/download/audios'
        return HttpMediarkReporter(
            self.config['domain'], tenant_provider,
            image_repository, audio_repository)
