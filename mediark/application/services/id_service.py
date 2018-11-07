import uuid
from abc import ABC, abstractmethod


class IdService(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        "Generate method to be implemented."


class StandardIdService(IdService):
    """ID service using the standard library uuid (v4) module."""

    def generate_id(self) -> str:
        return str(uuid.uuid4())
