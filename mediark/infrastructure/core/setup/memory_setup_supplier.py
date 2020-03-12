from typing import Dict, Any
from tenark.models import Tenant
from tenark.resolver import resolve_managers
from .setup_supplier import SetupSupplier


class MemorySetupSupplier(SetupSupplier):

    def setup(self):
        pass
