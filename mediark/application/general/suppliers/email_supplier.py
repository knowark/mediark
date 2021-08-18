from typing import Dict, Callable
from abc import ABC, abstractmethod
from ....application.domain.common import RecordList


class EmailSupplier(ABC):
    @abstractmethod
    async def send(self, payload: RecordList) -> None:
        """Send method to be implemented."""

class MemoryEmailSupplier(EmailSupplier):
    async def send(self, payload: RecordList) -> None:
        self._send = True
