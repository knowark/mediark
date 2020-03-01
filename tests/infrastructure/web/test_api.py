from typing import List
from pytest import fixture, raises
from aiohttp import web
from rapidjson import loads, dumps
from marshmallow import ValidationError
from base64 import b64encode
from mediark.application.models import Audio, Image
from mediark.infrastructure.core.configuration import SqlConfig
from mediark.infrastructure.web.resources import RootResource
from mediark.infrastructure.web.spec import create_spec
from mediark.infrastructure.core import (
    DevelopmentConfig, JsonConfig, SqlConfig, build_config, Config)


def test_build_configurations() -> None:
    config_path = ".config.json"
    config = build_config(config_path, "DEV")
    assert isinstance(config, DevelopmentConfig)
    config = build_config(config_path, "JSON")
    assert isinstance(config, JsonConfig)
    config = build_config(config_path, "PROD")
    assert isinstance(config, SqlConfig)


def test_development_config_retrieve(retrieve_development_conf) -> None:
    assert isinstance(retrieve_development_conf, SqlConfig)


async def test_root_resource(app: web.Application) -> None:
    response = await app.get('/')
    content = await response.text()
    assert response.status == 200
    assert 'Mediark' in content


async def test_root_resource_request_none(app: web.Application) -> None:
    response = await app.get('/?api')
    data = await response.text()
    api = loads(data)

    assert 'openapi' in api
    assert api['info']['title'] == 'Mediark'


async def test_invalid_headers(app: web.Application) -> None:
    response = await app.get('/audios')
    data = loads(await response.text())
    assert data["errors"]


async def test_bad_filter_get_route_filter(app, headers) -> None:
    response = await app.get('/images?filter=[[**BAD FILTER**]]',
                             headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert data_dict


async def test_api_images_put_search_and_download(
    app: web.Application, headers: dict, encoded_image: bytes
) -> None:
    custom_uuid = "932eff07-175a-44b5-871b-4bdaae6ad054"
    image = {'data': encoded_image, 'reference': custom_uuid,
             'extension': 'jpg', 'namespace': 'https://example.org'}
    response = await app.post('/images', data=dumps(image), headers=headers)

    assert response.status == 200

    response = await app.head('/images', headers=headers)
    assert int(response.headers.get('Total-Count')) > 0

    response = await app.get(
        f'/images?filter=[["reference", "=", "{custom_uuid}"]]',
        headers=headers)
    data = loads(await response.text())

    assert len(data) > 0

    download_url = "/"+data[0]['url'].split('/', 3)[3]
    response = await app.get(download_url, headers=headers)
    encoded_image_response = str(b64encode(await response.read()), 'utf-8')

    assert encoded_image == encoded_image_response


async def test_api_audios_put_search_and_download(
    app: web.Application, headers: dict, encoded_audio: bytes
) -> None:
    custom_uuid = "504773eb-2ff4-4dbd-87e7-f1bad231deee"
    audio = {'data': encoded_audio, 'reference': custom_uuid,
             'extension': 'mp3', 'namespace': 'https://example.org'}
    response = await app.post('/audios', data=dumps(audio), headers=headers)

    assert response.status == 200

    response = await app.head('/audios', headers=headers)
    assert int(response.headers.get('Total-Count')) > 0

    response = await app.get(
        f'/audios?filter=[["reference", "=", "{custom_uuid}"]]',
        headers=headers)
    data = loads(await response.text())

    assert len(data) > 0

    download_url = "/"+data[0]['url'].split('/', 3)[3]
    response = await app.get(download_url, headers=headers)
    encoded_audio_response = str(b64encode(await response.read()), 'utf-8')

    assert encoded_audio == encoded_audio_response
