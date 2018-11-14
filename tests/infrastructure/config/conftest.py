from json import dump
from pytest import fixture


@fixture(scope='session')
def config_file(tmpdir_factory):
    config_file = str(tmpdir_factory.mktemp(
        'config').join('mediark_config.json'))

    data = {
        'domain': 'mediark.knowark.com',
        'environment': {
            'media': '/var/opt/mediark/media',
            'shelve': '/var/opt/mediark/shelve'
        },
        'download': 'mediark.knowark.com/download',
    }

    with open(config_file, 'w') as f:
        dump(data, f)

    return config_file
