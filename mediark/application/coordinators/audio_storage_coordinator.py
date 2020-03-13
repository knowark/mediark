from ..models import Audio
from typing import List, Dict, Tuple, Any
from base64 import b64decode
from ..repositories import AudioRepository
from ..services import IdService, FileStoreService
from .types import RecordList


class AudioStorageCoordinator:
    def __init__(self, audio_repository: AudioRepository,
                 id_service: IdService,
                 file_store_service: FileStoreService) -> None:
        self.audio_repository = audio_repository
        self.id_service = id_service
        self.file_store_service = file_store_service

    async def store(self, audio_records: RecordList) -> None:
        contexts, audio_records = self._build_contexts(audio_records)
        audios = await self.audio_repository.add(
            [Audio(**audio_dict) for audio_dict in audio_records])

        uris = await self.file_store_service.store(contexts)
        for audio, uri in zip(audios, uris):
            audio.uri = uri

        await self.audio_repository.add(audios)

    def _build_contexts(self, audio_records: RecordList
                        ) -> Tuple[List[Dict[str, Any]], RecordList]:
        contexts: List[Dict[str, Any]] = []
        for audio_dict in audio_records:
            content = audio_dict.pop('data', None)
            if not content:
                raise ValueError("All the audios must have content.")
            audio_dict.setdefault('id', self.id_service.generate_id())
            contexts.append({'content': b64decode(content), **audio_dict})
        return contexts, audio_records
