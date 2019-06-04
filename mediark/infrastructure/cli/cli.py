from argparse import ArgumentParser, Namespace
from ..core.configuration import Config
# from ..resolver import Registry
from injectark import Injectark
from ..data import DirectoryArranger, ShelveArranger
from ..web import ServerApplication
from mediark.infrastructure.web.base import create_app


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
        # setup_parser = subparsers.add_parser('setup')
        # setup_parser.set_defaults(func=self.setup)

        # Provision
        provision_parser = subparsers.add_parser(
            'provision', help='Provision new tenants.')
        provision_parser.add_argument('data')
        provision_parser.set_defaults(func=self.provision)

        # Serve
        serve_parser = subparsers.add_parser(
            'serve', help='Start HTTP server.')
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

    def serve(self, args: Namespace) -> None:
        print('...SERVE:::', args)

        app = create_app(self.config, self.registry)
        gunicorn_config = self.config['gunicorn']
        ServerApplication(app, gunicorn_config).run()
