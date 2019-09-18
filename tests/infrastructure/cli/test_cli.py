from pytest import raises, fixture
from injectark import Injectark
from unittest.mock import Mock, call
from argparse import Namespace
from mediark.infrastructure.cli import cli as cli_module


def test_cli_instantiation(cli):
    assert cli is not None


def test_cli_run(cli):
    mock_parse = Mock()
    cli.parse = mock_parse
    argv = []
    cli.run(argv)

    assert mock_parse.call_count == 1


def test_cli_parse(cli):
    called = False
    argv = ['serve']
    result = cli.parse(argv)

    assert result is not None


def test_cli_parse_empty_argv(cli):
    with raises(SystemExit) as e:
        result = cli.parse([])


def test_cli_provision(cli, monkeypatch):
    namespace = Namespace()
    namespace.name = "custom"
    cli.provision(namespace)
    tenants = cli.resolver["TenantSupplier"].search_tenants("")

    assert len(tenants) == 2
    assert tenants[0]["name"] == "custom"

    print("TENANTS::::", tenants)


def test_cli_serve(cli, monkeypatch):
    called = False
    namespace = Namespace()

    called = False

    class MockServerApplication:
        def __init__(self, app, options):
            pass

        def run(self):
            nonlocal called
            called = True

    create_app_called = False

    def mock_create_app_function(config, resolver):
        nonlocal create_app_called
        create_app_called = True

    monkeypatch.setattr(
        cli_module, 'ServerApplication', MockServerApplication)
    monkeypatch.setattr(
        cli_module, 'create_app', mock_create_app_function)

    cli.serve(namespace)

    assert called and create_app_called
