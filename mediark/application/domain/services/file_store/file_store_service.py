from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any
from typing import Protocol, runtime_checkable


class FileStoreService(ABC):
    @abstractmethod
    async def store(self, contexts: List[Dict[str, Any]]) -> List[str]:
        "Store method to be implemented."

    @abstractmethod
    async def submit(self, contexts: List[Dict[str, Any]]) -> List[str]:
        "Submit method to be implemented."

    @abstractmethod
    async def load(self, uri: str, stream: 'Writer') -> None:
        "Load method to be implemented."


@runtime_checkable
class Writer(Protocol):
    async def write(self, data: bytes) -> None:
        "Write protocol method"


@runtime_checkable
class Reader(Protocol):
    async def read(self, size: int) -> bytes:
        "Read protocol method"
