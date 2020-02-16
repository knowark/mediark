import sys
import rapidjson as json
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from injectark import Injectark
from migrark import sql_migrate
from ..core.configuration import Config
from typing import List
from ..data import DirectoryArranger
from ..web import create_app, run_app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Cli:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        self.parser = ArgumentParser('Mediark')

    async def run(self, argv: List[str]):
        args = await self.parse(argv)
        await args.func(args)

    async def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

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

        # Migrate
        migrate_parser = subparsers.add_parser(
            'migrate', help='Upgrade tenant schema version.')
        migrate_parser.set_defaults(func=self.migrate)
        migrate_parser.add_argument(
            "-t", "--tenant", help="Target tenant to upgrade",
            required=True)
        migrate_parser.add_argument(
            "-v", "--version", help="Migration version to upgrade",
            required=True)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def migrate(self, args: Namespace) -> None:
        logger.info(f'MIGRATE: {vars(args)}')
        tenant_supplier = self.injector['TenantSupplier']
        tenant = tenant_supplier.resolve_tenant(args.tenant)
        zone = tenant['zone'] or 'default'

        database_uri = self.config['zones'][zone]['dsn']
        migrations_path = str((Path(__file__).parent.parent / 'data' /
                               'sql' / 'migrations').absolute())
        sql_migrate(database_uri, migrations_path, schema=tenant['slug'],
                    target_version=args.version)
        logger.info('END MIGRATE')

    async def provision(self, args: Namespace) -> None:
        logger.info('PROVISION')
        tenant_supplier = self.injector.resolve('TenantSupplier')
        tenant_dict = json.loads(args.data)
        logger.info("Creating tenant:", tenant_dict)
        tenant_supplier.create_tenant(tenant_dict)
        logger.info('END PROVISION')

    async def serve(self, args: Namespace) -> None:
        logger.info('SERVE')
        port = args.port or self.config['port']
        app = create_app(self.config, self.injector)
        await run_app(app, port)
        logger.info('END SERVE')
