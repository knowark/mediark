from argparse import ArgumentParser, Namespace
from ..config import Config
from ..web import create_app, ServerApplication


class Cli:
    def __init__(self, config: Config) -> None:
        self.registry = None
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
        print('...SETUP:::', args)

    def serve(self, args: Namespace) -> None:
        print('...SERVE:::', args)

        app = create_app(self.context)
        gunicorn_config = self.config['gunicorn']
        ServerApplication(app, gunicorn_config).run()
