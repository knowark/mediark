import io
from json import loads, dumps
from aiohttp import FormData
from mediark.presentation.platform.rest import RestApplication
from mediark.presentation.platform.rest import rest as rest_module


async def test_rest_application_run(monkeypatch):
    called = False

    class web:
        @staticmethod
        async def _run_app(app, port=1234):
            nonlocal called
            called = True

    monkeypatch.setattr(rest_module, 'web', web)

    await RestApplication.run(None)

    assert called is True


# Root

async def test_root(app) -> None:
    response = await app.get('/favicon')
    response = await app.get('/')

    content = await response.text()

    assert response.status == 200
    assert 'Mediark' in content


async def test_root_api(app) -> None:
    response = await app.get('/?api')
    data = await response.text()
    api = loads(data)

    assert 'openapi' in api
    assert api['info']['title'] == 'Mediark'


# Medias

async def test_media_head(app, headers) -> None:
    response = await app.head('/media', headers=headers)
    count = response.headers.get('Count')
    print("TEST REST>>>"*50)
    print(count)
    assert int(count) == 3


async def test_media_get(app, headers) -> None:
    response = await app.get('/media', headers=headers)
    content = await response.text()
    assert response.status == 200
    data_dict = loads(content)['data']
    assert len(data_dict) == 3


async def test_media_patch(app, headers) -> None:
    custom_uuid = "932eff07-175a-44b5-871b-4bdaae6ad054"
    base64data = 'SU1BR0VfREFUQQ=='
    image = dumps({
                    "meta":{},
                    "data": [{
                        'data': base64data,
                        'type': 'images',
                        'reference': custom_uuid
                        }]
                  })


    response = await app.patch('/media', data=image, headers=headers)
    assert response.status == 200


async def test_media_delete(app, headers) -> None:
    data = {"data": ["932eff07-175a-44b5-871b-4bdaae6ad054"]}
    response = await app.delete('/media', data=dumps(data), headers=headers)
    assert response.status == 200


async def test_media_delete_url(app, headers) -> None:
    id_ = "932eff07-175a-44b5-871b-4bdaae6ad054"
    response = await app.delete(f'/media/{id_}', headers=headers)
    assert response.status == 200


# Downloads


async def test_api_download_get(app, headers) -> None:
    tenant = 'default'
    path = "path_1"
    response = await app.get(f'/download/{tenant}/{path}', headers=headers)
    assert response.status == 200


# Uploads


async def test_api_upload_put(app, headers) -> None:
    file = io.StringIO('Mock In-Memory File')

    data = FormData()
    data.add_field(
        'media', '{"id": "ABC123"}', content_type='application/json')
    data.add_field(
        'file', file, content_type='text/plain')

    response = await app.put('/upload', headers=headers, data=data)
    assert response.status == 200


# Filters


async def test_filter_get_route_filter(app, headers) -> None:
    response = await app.get(
        '/media?filter=[["reference", "=", "ref_1"]]',
        headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 1


async def test_filter_get_route_filter(app, headers) -> None:
    response = await app.get(
        '/media?filter=[["reference", "=", "ref_1"]]',
        headers=headers)
    content = await response.text()
    print("TEST FILTER>>>>"*50)
    print(content)
    data_dict = loads(content)
    assert len(data_dict) == 1


async def test_get_request_filter(app, headers) -> None:
    response = await app.get(
        '/media?filter=[[]]',
        headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 1


async def test_bad_filter_get_route_filter(app, headers) -> None:
    response = await app.get('/media?filter=[[**BAD FILTER**]]',
                             headers=headers)
    content = await response.text()
    data_dict = loads(content)['data']
    assert len(data_dict) == 3


async def test_users_get_route_filter(app, headers) -> None:
    response = await app.get(
        '/devices?filter=[["createdAt", "=", 9999999999]]',
        headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 1

# middleware


async def test_media_get_unauthorized(app) -> None:
    response = await app.get('/media')
    content = await response.text()

    assert response.status == 401
    data_dict = loads(content)
    assert 'errors' in data_dict
