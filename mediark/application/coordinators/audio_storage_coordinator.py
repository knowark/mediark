from ..models import Audio
from typing import Optional, List
from base64 import b64decode
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

    async def store(self, audio_dict: AudioDict) -> None:
        content = audio_dict.pop('data', None)
        if not content:
            raise ValueError("The audio must have content.")

        audio_dict.setdefault('id', self.id_service.generate_id())
        audio, *_ = await self.audio_repository.add(Audio(**audio_dict))

        content_bytes = b64decode(content)
        context = {'type': 'audios', **vars(audio), 'content': content_bytes}

        uri = await self.file_store_service.store(context)

        audio.uri = uri
        await self.audio_repository.add(audio)
