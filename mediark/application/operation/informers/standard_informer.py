from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from ...domain.models import Media
from ...domain.services import RepositoryService
from ...domain.common.types import RecordList, QueryDomain
from ..common import dump


class StandardInformer:
    def __init__(self, repository_service: RepositoryService) -> None:
        self.repository_service = repository_service

    async def search(self, entry: dict) -> dict:
        meta = entry['meta']
        repository = self.repository_service.resolve(meta.pop('model'))
        result = await repository.search(**meta)
        return {'data': [dump(item) for item in result]}

    async def count(self, entry: dict) -> dict:
        meta = entry['meta']
        repository = self.repository_service.resolve(meta.pop('model'))
        result = await repository.count(meta['domain'])
        return {'data': result}
