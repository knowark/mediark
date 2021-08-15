from typing import List
from abc import ABC, abstractmethod


class MigrationSupplier(ABC):
    @abstractmethod
    def migrate(self, tenant: str = '', version: str = '') -> None:
        """Migrate method to be implemented."""


class MemoryMigrationSupplier(MigrationSupplier):
    def migrate(self, tenant: str = '', version: str = '') -> None:
        self._migrated = True
