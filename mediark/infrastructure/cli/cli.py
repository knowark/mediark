import sys
import json
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from ..core.configuration import Config
from typing import List
from ..data import DirectoryArranger, ShelveArranger
from ..web import create_app, ServerApplication


class Cli:
    def __init__(self, config: Config, resolver: Injectark) -> None:
        self.config = config
        self.resolver = resolver
        self.registry = resolver
        self.parser = ArgumentParser('Mediark')

    def run(self, argv: List[str]):
        args = self.parse(argv)
        args.func(args)

    def parse(self, argv: List[str]) -> Namespace:
        subparsers = self.parser.add_subparsers()

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('data')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
        serve_parser.set_defaults(func=self.serve)

        if len(argv) == 0:
            self.parser.print_help()
            self.parser.exit()

        return self.parser.parse_args(argv)

    def provision(self, args: Namespace) -> None:
        print('...PROVISION::::')
        tenant_supplier = self.resolver.resolve('TenantSupplier')
        tenant_dict = {'name': args.name}
        tenant_supplier.create_tenant(tenant_dict)
        print('END PROVISION |||||')

    def serve(self, args: Namespace) -> None:
        print('...:::SERVE:::...', args, '\n')

        app = create_app(self.config, self.resolver)
        ServerApplication(app, self.config['gunicorn']).run()
