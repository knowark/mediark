from json import loads
from typing import List
from uuid import uuid4
from pytest import fixture, raises
from json import loads, dumps
from flask import Flask, request
from marshmallow import ValidationError
from mediark.application.models import Audio, Image
from mediark.infrastructure.core.configuration import ProductionConfig
from mediark.infrastructure.web.resources import RootResource
from mediark.infrastructure.web.spec import create_spec


def test_production_config_retrieve(retrieve_production_conf) -> None:
    assert isinstance(retrieve_production_conf, ProductionConfig)


def test_root_resource(app: Flask, headers: dict) -> None:
    response = app.get('/', headers=headers)
    data = str(response.data, 'utf-8')
    assert data is not None


def test_root_resource_request_none(app: Flask, headers: dict) -> None:
    response = app.get('/?api', headers=headers)
    data = str(response.data, 'utf-8')
    assert data is not None


def test_invalid_headers(app: Flask) -> None:
    response = app.get('/audio')
    data = loads(str(response.data, 'utf-8'))
    assert data["error"]


def test_api_images_put_and_search(
    app: Flask, headers: dict, encoded_image: bytes
) -> None:
    image = {'data': str(encoded_image), 'reference': 'ABC',
             'extension': 'jpg', 'namespace': 'https://example.org'}
    response = app.post('/images', data=dumps(image), headers=headers,
                        content_type='application/json')

    assert response.status == "201 CREATED"

    response = app.get(
        '/images?filter=[["reference", "=", "ABC"]]', headers=headers)
    print("RESPONSE DATA:::: ", response.data)
    data = loads(str(response.data, 'utf-8'))

    assert len(data) == 1


def test_api_audios_put_and_search(
    app: Flask, headers: dict, encoded_audio: bytes
) -> None:

    audio = {'data': str(encoded_audio), 'reference': 'XYZ',
             'extension': 'jpg', 'namespace': 'https://example.org'}
    response = app.post('/audios', data=dumps(audio), headers=headers,
                        content_type='application/json')

    assert response.status == "201 CREATED"

    response = app.get(
        '/audios?filter=[["reference", "=", "XYZ"]]', headers=headers)
    data = loads(str(response.data, 'utf-8'))
    assert len(data) == 1
