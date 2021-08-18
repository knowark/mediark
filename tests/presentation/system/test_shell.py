import json
from typing import List
from unittest.mock import AsyncMock
from pytest import fixture, raises
from injectark import Injectark
from mediark.integration.factories import factory_builder
from mediark.presentation.system import Shell
from mediark.presentation.system import shell as shell_module
from mediark.integration.core import config


@fixture
def shell() -> Shell:
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)

    return Shell(injector)


def test_shell_instantiation(shell):
    assert shell is not None


async def test_shell_run(shell):
    mock_parse = AsyncMock()
    shell.parse = mock_parse
    argv: List = []
    await shell.run(argv)

    assert mock_parse.call_count == 1


async def test_shell_parse(shell):
    called = False
    argv = ['serve']
    result = await shell.parse(argv)

    assert result is not None


async def test_shell_parse_empty_argv(shell):
    with raises(SystemExit) as e:
        result = await shell.parse([])


async def test_shell_serve(shell, monkeypatch):
    called = False
    custom_port = None

    class MockRestApplication:
        def __init__(self, injector):
            pass

        @staticmethod
        async def run(app, port):
            nonlocal called, custom_port
            called = True
            custom_port = port

    monkeypatch.setattr(
        shell_module, 'RestApplication', MockRestApplication)

    await shell.serve({
        'port': '9201'
    })

    assert called and called
    assert custom_port == 9201


async def test_shell_provision(shell):
    options = {
        'data': json.dumps({
            'id': '001',
            'name': 'Knowark'
        })
    }

    result = await shell.provision(options)

    assert result is None

async def test_shell_operate(shell):
    options = {
        'operation': 'EmailManager.send',
        'entry': json.dumps({
            'meta': {
                "model": "Email"
            },
            'data':
                [{
                    "template": "mail/auth/activation.html",
                    "context": {
                        "type": "activation",
                        "subject": "New Account Activation",
                        "recipient": "valenep@example.com",
                        "owner": "Valentina",
                        "token": "<verification_token>"
                    }
                }]

            }
        )
    }

    result = await shell.operate(options)

    assert result is None
