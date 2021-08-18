from typing import Dict, Callable
from abc import ABC, abstractmethod


class EmailSupplier(ABC):
    @abstractmethod
    async def send(self, payload: dict) -> None:
        """Send method to be implemented."""

class MemoryEmailSupplier(EmailSupplier):
    async def send(self, payload: dict) -> None:
        self._send = True
