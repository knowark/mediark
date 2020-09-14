import json
import logging
from typing import Dict
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from typing import List
from ...core import Config
from ..rest import RestApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Shell:
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        self.parser = ArgumentParser('Authark')

    async def run(self, argv: List[str]):
        args = await self.parse(argv)
        await args.func(vars(args))

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
        # migrate_parser = subparsers.add_parser(
        # 'migrate', help='Upgrade tenant schema version.')
        # migrate_parser.set_defaults(func=self.migrate)
        # migrate_parser.add_argument(
        # "-t", "--tenant", help="Target tenant to upgrade",
        # required=True)
        # migrate_parser.add_argument(
        # "-v", "--version", help="Migration version to upgrade",
        # default='999')

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    async def serve(self, options: Dict[str, str]) -> None:
        logger.info('SERVE')
        port = int(options.get('port') or self.config['port'])
        app = RestApplication(self.config, self.injector)
        await RestApplication.run(app, port)
        logger.info('END SERVE')

    async def provision(self, options: Dict[str, str]) -> None:
        logger.info('PROVISION')
        tenant_supplier = self.injector.resolve('TenantSupplier')
        tenant_dict = json.loads(options['data'])
        logger.info("Creating tenant:", tenant_dict)
        tenant_supplier.ensure_tenant(tenant_dict)
        logger.info('END PROVISION')

    # async def migrate(self, options: Dict[str, str]) -> None:
        # logger.info(f'MIGRATE: {options}')
        # tenant_supplier = self.injector['TenantSupplier']
        # tenant = tenant_supplier.resolve_tenant(options['tenant'])
        # zone = tenant['zone'] or 'default'

        # database_uri = self.config['zones'][zone]['dsn']
        # migrations_path = str((Path(__file__).parent.parent / 'data' /
        # 'sql' / 'migrations').absolute())
        # sql_migrate(database_uri, migrations_path, schema=tenant['slug'],
        # target_version=options['version'])
        # logger.info('END MIGRATE')
