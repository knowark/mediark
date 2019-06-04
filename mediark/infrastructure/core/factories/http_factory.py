from ....application.repositories import ImageRepository, AudioRepository
from ...http import HttpMediarkReporter
from ...config import Config
from .directory_factory import DirectoryFactory


class HttpFactory(DirectoryFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def http_mediark_reporter(self, image_repository: ImageRepository,
                              audio_repository: AudioRepository
                              ) -> HttpMediarkReporter:
        image_download = self.config['domain'] + '/download/images'
        audio_download = self.config['domain'] + '/download/audios'
        return HttpMediarkReporter(
            image_download, audio_download,
            image_repository, audio_repository)