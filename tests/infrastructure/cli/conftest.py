# from pytest import fixture
# from injectark import Injectark
# from mediark.infrastructure.core import Config, DevelopmentConfig
# from mediark.infrastructure.core.factories import build_factory
# from mediark.infrastructure.cli import Cli


# @fixture
# def cli() -> Cli:
#     config = DevelopmentConfig()
#     strategy = config["strategy"]
#     factory = build_factory(config)

#     resolver = Injectark(strategy, factory)

#     return Cli(config, resolver)
