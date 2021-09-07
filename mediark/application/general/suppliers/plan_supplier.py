from typing import Dict, Callable
from abc import ABC, abstractmethod


class PlanSupplier(ABC):
    @abstractmethod
    async def setup(self) -> None:
        """Setup method to be implemented."""

    @abstractmethod
    async def defer(self, job: str, payload: Dict = None) -> None:
        """Defer method to be implemented."""


class MemoryPlanSupplier(PlanSupplier):
    async def setup(self) -> None:
        self._setup = True

    async def defer(self, job: str, payload: Dict = None) -> None:
        self._job = job
        self._payload = payload
