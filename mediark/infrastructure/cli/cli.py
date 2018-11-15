from argparse import ArgumentParser, Namespace
from ..config import Config
from ..resolver import Registry
from ..data import DirectoryArranger, ShelveArranger
from ..web import create_app, ServerApplication


class Cli:
    def __init__(self, config: Config, registry: Registry) -> None:
        self.registry = registry
        self.config = config

        args = self.parse()
        args.func(args)

    def parse(self) -> Namespace:
        parser = ArgumentParser('Mediark')
        subparsers = parser.add_subparsers()

        # Setup
        setup_parser = subparsers.add_parser('setup')
        setup_parser.set_defaults(func=self.setup)

        # Serve
        serve_parser = subparsers.add_parser('serve')
        serve_parser.set_defaults(func=self.serve)

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
