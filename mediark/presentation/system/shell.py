import json
import logging
from typing import Dict
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List
from ...integration.core import Config
from ..platform.rest import RestApplication
from .scheduler import Scheduler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Shell:
    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.config = injector.config
        self.parser = ArgumentParser('Authark')

    async def run(self, argv: List[str]):
        args = await self.parse(argv)
        await args.func(vars(args))

    async def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Prepare
        prepare_parser = subparsers.add_parser(
            'prepare', help='Prepare the application infrastructure.')
        prepare_parser.set_defaults(func=self.prepare)

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('data', help='JSON encoded tenant.')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.add_argument('-p', '--port')
        serve_parser.set_defaults(func=self.serve)

        # Work
        work_parser = subparsers.add_parser(
            'work', help='Start background worker.')
        work_parser.set_defaults(func=self.work)

        # Time
        time_parser = subparsers.add_parser(
            'time', help='Start system timer.')
        time_parser.set_defaults(func=self.time)

        # Schedule
        schedule_parser = subparsers.add_parser(
            'schedule', help='Start scheduler.')
        schedule_parser.add_argument('-w', '--work', action='store_true')
        schedule_parser.add_argument('-t', '--time', action='store_true')
        schedule_parser.set_defaults(func=self.schedule)

        # Operate
        operate_parser = subparsers.add_parser(
            'operate', help='Enter Operations.')
        operate_parser.add_argument('operation')
        operate_parser.add_argument('entry')
        operate_parser.set_defaults(func=self.operate)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def prepare(self, options: Dict[str, str]) -> None:
        logger.info('PREPARE')
        await self.injector['SessionManager'].set_system({})
        await self.injector['SetupManager'].prepare({})
        logger.info('END PREPARE')

    async def serve(self, options: Dict[str, str]) -> None:
        logger.info('SERVE')
        port = int(options.get('port') or self.config['port'])
        app = RestApplication(self.injector)
        await RestApplication.run(app, port)
        logger.info('END SERVE')

    async def work(self, options_dict: Dict[str, str]) -> None:
        logger.info('WORK')
        await Scheduler(self.injector).run(options_dict)
        logger.info('END WORK')

    async def time(self, options_dict: Dict[str, str]) -> None:
        logger.info('TIME')
        await Scheduler(self.injector).run({'time': True})
        logger.info('END TIME')

    async def provision(self, options: Dict[str, str]) -> None:
        logger.info('PROVISION')
        tenant_dict = json.loads(options['data'])
        logger.info("Creating tenant:", tenant_dict)
        await self.injector['SessionManager'].ensure_tenant(tenant_dict)
        logger.info('END PROVISION')

    async def schedule(self, options: Dict[str, str]) -> None:
        logger.info('SCHEDULE')
        scheduler = Scheduler(self.injector)
        await scheduler.run(options)
        logger.info('END SCHEDULE')

    async def operate(self, options: Dict[str, str]) -> None:
        session_manager = self.injector['SessionManager']
        await session_manager.set_system({})
        manager, method = options['operation'].split('.')
        entry = json.loads(options['entry'])
        result = await getattr(self.injector[manager], method)(entry)
        logger.info(json.dumps(result, indent=2))

