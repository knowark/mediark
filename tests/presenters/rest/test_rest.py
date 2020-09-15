from json import loads, dumps
from mediark.presenters.rest import RestApplication
from mediark.presenters.rest import rest as rest_module


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


async def test_root(app) -> None:
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


async def test_filter_get_route_filter(app, headers) -> None:
    response = await app.get(
        '/medias?filter=[["reference", "=", "ref_1"]]',
        headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 1


async def test_bad_filter_get_route_filter(app, headers) -> None:
    response = await app.get('/medias?filter=[[**BAD FILTER**]]',
                             headers=headers)
    content = await response.text()
    data_dict = loads(content)
    assert len(data_dict) == 3


async def test_media_get(app, headers) -> None:
    response = await app.get('/medias', headers=headers)
    content = await response.text()
    assert response.status == 200
    data_dict = loads(content)
    assert len(data_dict) == 3


async def test_media_head(app, headers) -> None:
    response = await app.head('/medias', headers=headers)
    count = response.headers.get('Total-Count')

    assert int(count) == 3


async def test_api_media_put(app, headers) -> None:
    custom_uuid = "932eff07-175a-44b5-871b-4bdaae6ad054"
    base64data = b'SU1BR0VfREFUQQ=='
    image = [{'data': base64data, 'type': 'images', 'reference': custom_uuid,
              'extension': 'jpg', 'namespace': 'https://example.org'}]

    response = await app.put('/medias', data=dumps(image), headers=headers)
    assert response.status == 200


async def test_api_download_get(app, headers) -> None:
    uri = "2020/03/11/7439edb5-c38f-4dc6-9d8f-89b6d67a6c6d.jpg"
    response = await app.get('/downloads/{uri}', headers=headers)
    assert response.status == 200
