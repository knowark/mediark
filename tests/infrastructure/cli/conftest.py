from pytest import fixture
from injectark import Injectark
from mediark.infrastructure.core.configuration import Config, JsonConfig
from mediark.infrastructure.core.factories import build_factory
from mediark.infrastructure.cli import Cli


@fixture
def cli(tmp_path) -> Cli:
    config = JsonConfig()
    config['tenancy']['json'] = str(tmp_path / 'tenants.json')
    config['data']['dir_path'] = str(tmp_path / 'data')
    template_dir = tmp_path / 'data' / '__template__'
    template_dir.mkdir(parents=True, exist_ok=True)
    config['secrets']['jwt'] = str(tmp_path / 'sign.txt')
    config['secrets']['domain'] = str(tmp_path / 'domain.txt')
    with open(config['secrets']['jwt'], "w") as f:
        f.write("123456")
    strategy = config["strategy"]
    factory = build_factory(config)

    resolver = Injectark(strategy, factory)

    return Cli(config, resolver)
