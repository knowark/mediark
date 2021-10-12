import asyncpg
import schedulark
from injectark import Config, Injectark
from .jobs import JOBS


class Scheduler:
    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.config = injector.config
        self.session_manager = self.injector['SessionManager']

    async def run(self, options: dict) ->None:
        await self.session_manager.set_system({})

        dsn = self.config['scheduler']['dsn']
        pool = await asyncpg.create_pool(dsn=dsn)
        queue = schedulark.SqlQueue(Connector(pool))
        scheduler = schedulark.Scheduler(queue)

        for job in JOBS:
            scheduler.register(job(self.injector))

        if options.get('time'):
            return await scheduler.time()

        return await scheduler.work()


class Connector:
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        self.pool = pool

    async def get(self):
        return self.pool
