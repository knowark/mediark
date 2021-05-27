from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Protocol


class FileStoreService(ABC):
    @abstractmethod
    async def submit(self, contexts: List[Dict[str, Any]]) -> List[str]:
        "Submit method to be implemented."

    @abstractmethod
    async def load(self, uri: str, stream: 'Writer') -> None:
        "Load method to be implemented."

    @abstractmethod
    async def delete(self, uri: str) -> None:
        "Delete method to be implemented."


class Writer(Protocol):
    async def setup(self, config: Dict[str, Any]) -> None:
        "Setup write method"

    async def write(self, data: bytes) -> None:
        "Write protocol method"


class Reader(Protocol):
    async def setup(self, config: Dict[str, Any]) -> None:
        "Setup read method"

    async def read(self, size: int) -> bytes:
        "Read protocol method"
