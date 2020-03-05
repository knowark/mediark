from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union, Any


class FileStoreService(ABC):
    @abstractmethod
    async def store(self, content: bytes,
                    context: Dict[str, str]) -> str:
        "Store method to be implemented."

    @abstractmethod
    async def load(self, uri: str) -> Tuple[bytes, Dict[str, Any]]:
        "Load method to be implemented."
