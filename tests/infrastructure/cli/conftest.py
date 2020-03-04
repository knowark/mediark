from pytest import fixture
from injectark import Injectark
from mediark.infrastructure.core import build_config
from mediark.infrastructure.factories import build_strategy, build_factory
from mediark.infrastructure.cli import Cli


@fixture
def cli(tmp_path) -> Cli:
    config = build_config('', 'DEV')
    config['tenancy']['json'] = str(tmp_path / 'tenants.json')
    config['data']['dir_path'] = str(tmp_path / 'data')
    template_dir = tmp_path / 'data' / '__template__'
    template_dir.mkdir(parents=True, exist_ok=True)

    factory = build_factory(config)
    strategy = build_strategy(config['strategies'], config["strategy"])

    resolver = Injectark(strategy, factory)

    return Cli(config, resolver)
