import sys
import json
from argparse import ArgumentParser, Namespace
from injectark import Injectark
from ..core.configuration import Config
from ..data import DirectoryArranger, ShelveArranger
from ..web import create_app, ServerApplication


class Cli:
    def __init__(self, config: Config, resolver: Injectark) -> None:
        self.config = config
        self.resolver = resolver
        self.registry = resolver

        args = self.parse()
        args.func(args)

    def parse(self) -> Namespace:
        parser = ArgumentParser('Mediark')
        subparsers = parser.add_subparsers()

        # Setup
        setup_parser = subparsers.add_parser('setup')
        setup_parser.set_defaults(func=self.setup)

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('data')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser('serve')
        serve_parser.set_defaults(func=self.serve)

        if len(sys.argv[1:]) == 0:
            parser.print_help()
            parser.exit()

        return parser.parse_args()

    def setup(self, args: Namespace) -> None:
        print('SETUP IMAGE SHELVE FILE')
        image_shelve_file = (
            self.config['shelve'] + self.config['images']['shelve'])
        print(image_shelve_file)
        ShelveArranger.make_shelve(image_shelve_file)

        print('SETUP IMAGE MEDIA DIRECTORIES')
        images_media_directory = (
            self.config['media'] + self.config['images']['media'])
        print(images_media_directory)
        DirectoryArranger(images_media_directory).setup()

        print('SETUP AUDIO SHELVE FILE')
        audio_shelve_file = (
            self.config['shelve'] + self.config['audios']['shelve'])
        print(audio_shelve_file)
        ShelveArranger.make_shelve(audio_shelve_file)

        print('SETUP AUDIO MEDIA DIRECTORIES')
        audios_media_directory = (
            self.config['media'] + self.config['audios']['media'])
        print(audios_media_directory)
        DirectoryArranger(audios_media_directory).setup()
    
    def provision(self, args: Namespace) -> None:
        print('...PROVISION::::')
        tenant_supplier = self.resolver.resolve('TenantSupplier')
        tenant_dict = json.loads(args.data)
        tenant_supplier.create_tenant(tenant_dict)
        print('END PROVISION |||||')

    def serve(self, args: Namespace) -> None:
        print('...:::SERVE:::...', args, '\n')

        app = create_app(self.config, self.resolver)
        gunicorn_config = self.config['gunicorn']
        ServerApplication(app, gunicorn_config).run()
