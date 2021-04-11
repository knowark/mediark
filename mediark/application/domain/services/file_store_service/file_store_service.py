from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any


class FileStoreService(ABC):
    @abstractmethod
    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        "Store method to be implemented."

    @abstractmethod
    async def load(self, uri: str) -> Tuple[bytes, Dict[str, Any]]:
        "Load method to be implemented."
