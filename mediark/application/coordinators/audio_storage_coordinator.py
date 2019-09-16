from ..models import Audio
from ..repositories import AudioRepository
from ..services import IdService, FileStoreService
from .types import AudioDict


class AudioStorageCoordinator:
    def __init__(self, audio_repository: AudioRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.audio_repository = audio_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    def store(self, audio_dict: AudioDict) -> None:
        if 'data' not in audio_dict:
            return

        if 'id' not in audio_dict:
            audio_dict['id'] = self.id_service.generate_id()

        file_id = str(audio_dict.get('id'))
        content = audio_dict.pop('data')
        extension = audio_dict.get('extension')

        uri = self.file_store_service.store(file_id, content, extension)
        audio_dict['uri'] = uri
        audio = Audio(**audio_dict)
        self.audio_repository.add(audio)
