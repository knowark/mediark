from json import loads
from typing import List
from uuid import uuid4
from pytest import fixture, raises
from json import loads, dumps
from flask import Flask, request
from marshmallow import ValidationError
from base64 import b64encode
from mediark.application.models import Audio, Image
from mediark.infrastructure.core.configuration import DevelopmentConfig
from mediark.infrastructure.web.resources import RootResource
from mediark.infrastructure.web.spec import create_spec


def test_development_config_retrieve(retrieve_development_conf) -> None:
    assert isinstance(retrieve_development_conf, DevelopmentConfig)


def test_root_resource(app: Flask, headers: dict) -> None:
    response = app.get('/', headers=headers)
    data = str(response.data, 'utf-8')
    assert data is not None


def test_root_resource_request_none(app: Flask, headers: dict) -> None:
    response = app.get('/?api', headers=headers)
    data = str(response.data, 'utf-8')
    assert data is not None


def test_invalid_headers(app: Flask) -> None:
    response = app.get('/audios')
    data = loads(str(response.data, 'utf-8'))
    assert data["error"]


def test_api_images_put_search_and_download(
    app: Flask, headers: dict, encoded_image: bytes
) -> None:
    custom_uuid = str(uuid4())
    image = {'data': encoded_image, 'reference': custom_uuid,
             'extension': 'jpg', 'namespace': 'https://example.org'}
    response = app.post('/images', data=dumps(image), headers=headers,
                        content_type='application/json')

    print("Response:::", response)

    assert response.status == "201 CREATED"

    response = app.get(
        f'/images?filter=[["reference", "=", "{custom_uuid}"]]',
        headers=headers)
    data = loads(str(response.data, 'utf-8'))

    assert len(data) == 1

    download_url = "/"+data[0]['url'].split('/', 3)[3]
    response = app.get(download_url, headers=headers)
    encoded_image_response = str(b64encode(response.data), 'utf-8')

    assert encoded_image == encoded_image_response


def test_api_audios_put_search_and_download(
    app: Flask, headers: dict, encoded_audio: bytes
) -> None:

    audio = {'data': encoded_audio, 'reference': 'XYZ',
             'extension': 'jpg', 'namespace': 'https://example.org'}
    response = app.post('/audios', data=dumps(audio), headers=headers,
                        content_type='application/json')

    assert response.status == "201 CREATED"

    response = app.get(
        '/audios?filter=[["reference", "=", "XYZ"]]', headers=headers)
    data = loads(str(response.data, 'utf-8'))

    assert len(data) == 1

    download_url = "/"+data[0]['url'].split('/', 3)[3]
    response = app.get(download_url, headers=headers)
    encoded_audio_response = str(b64encode(response.data), 'utf-8')

    assert encoded_audio == encoded_audio_response
