# from typing import List
# from pytest import fixture, raises
# from aiohttp import web
# from rapidjson import loads, dumps
# from marshmallow import ValidationError
# from base64 import b64encode
# from mediark.infrastructure.web.resources import RootResource
# from mediark.infrastructure.web.spec import create_spec
# from mediark.infrastructure.config import (
#     DevelopmentConfig, ProductionConfig, build_config, Config)


# def test_build_configurations() -> None:
#     config_path = ".config.json"
#     config = build_config("DEV", config_path)
#     assert isinstance(config, DevelopmentConfig)
#     config = build_config("PROD", config_path)
#     assert isinstance(config, ProductionConfig)


# async def test_root_resource(app: web.Application) -> None:
#     response = await app.get('/')
#     content = await response.text()
#     assert response.status == 200
#     assert 'Mediark' in content


# async def test_root_resource_request_none(app: web.Application) -> None:
#     response = await app.get('/?api')
#     data = await response.text()
#     api = loads(data)

#     assert 'openapi' in api
#     assert api['info']['title'] == 'Mediark'


# async def test_invalid_headers(app: web.Application) -> None:
#     response = await app.get('/media')
#     data = loads(await response.text())
#     assert data["errors"]


# async def test_filter_get_route_filter(app, headers) -> None:
#     response = await app.get(
#         '/media?filter=[["reference", "=", "ref_1"]]',
#         headers=headers)
#     content = await response.text()
#     data_dict = loads(content)
#     assert len(data_dict) == 1


# async def test_bad_filter_get_route_filter(app, headers) -> None:
#     response = await app.get('/media?filter=[[**BAD FILTER**]]',
#                              headers=headers)
#     content = await response.text()
#     data_dict = loads(content)
#     assert len(data_dict) == 3


# async def test_api_media_get(app: web.Application, headers: dict) -> None:
#     response = await app.get('/media', headers=headers)
#     content = await response.text()
#     assert response.status == 200
#     data_dict = loads(content)
#     assert len(data_dict) == 3


# async def test_media_head(app, headers) -> None:
#     response = await app.head('/media', headers=headers)
#     count = response.headers.get('Total-Count')

#     assert int(count) == 3


# async def test_api_media_put(
#         app: web.Application, headers: dict) -> None:
#     custom_uuid = "932eff07-175a-44b5-871b-4bdaae6ad054"
#     base64data = b'SU1BR0VfREFUQQ=='
#     image = [{'data': base64data, 'type': 'images', 'reference': custom_uuid,
#               'extension': 'jpg', 'namespace': 'https://example.org'}]

#     response = await app.put('/media', data=dumps(image), headers=headers)
#     assert response.status == 200


# async def test_api_download_get(
#         app: web.Application, headers: dict) -> None:
#     uri = "2020/03/11/7439edb5-c38f-4dc6-9d8f-89b6d67a6c6d.jpg"
#     response = await app.get('/download/{uri}', headers=headers)
#     assert response.status == 200
