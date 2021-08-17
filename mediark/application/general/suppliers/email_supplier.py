from typing import Dict, Callable
from abc import ABC, abstractmethod


class EmailSupplier(ABC):
    @abstractmethod
    async def process(self, tenant: str, email: dict) -> None:
        """Process method to be implemented."""

class MemoryEmailSupplier(EmailSupplier):
    async def process(self, tenant: str, email: dict) -> None:
        self._process = True
