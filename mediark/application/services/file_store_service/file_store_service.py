from abc import ABC, abstractmethod
from typing import Dict, Union


class FileStoreService(ABC):
    @abstractmethod
    async def store(self, content: bytes,
                    context: Dict[str, str]) -> str:
        "Store method to be implemented."
