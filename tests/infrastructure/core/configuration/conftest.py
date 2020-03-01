import os
from json import dump
from pytest import fixture
from datetime import datetime
from typing import cast, List
from injectark import Injectark
from mediark.infrastructure.core import build_config, build_factory, Config
from mediark.infrastructure.web import create_app
from uuid import uuid4


@fixture(scope='session')
def config_file(tmpdir_factory):
    config_file = str(tmpdir_factory.mktemp(
        'config').join('mediark_config.json'))

    data = {
        'domain': 'mediark.knowark.com',
        'media': '/var/opt/mediark/media',
        'shelve': '/var/opt/mediark/shelve'
    }

    with open(config_file, 'w') as f:
        dump(data, f)

    return config_file
