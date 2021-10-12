from typing import Callable, Dict
from schedulark import Planner, SqlQueue
from .....application.general.suppliers import PlanSupplier
from .....application.general.connector import Connector


class SqlPlanSupplier(PlanSupplier):
    def __init__(self, connector: Connector) -> None:
        self.scheduler = Planner(SqlQueue(connector))

    async def setup(self) -> None:
        await self.scheduler.setup()

    async def defer(self, job: str, data: Dict = None) -> None:
        await self.scheduler.defer(job, data)
