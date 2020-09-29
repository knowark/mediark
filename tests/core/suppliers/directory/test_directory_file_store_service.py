from pytest import raises, fixture
from pathlib import Path
from base64 import b64decode


@fixture
def base_path(directory_file_store_service):
    base_path = Path("{0}/{1}/{2}".format(
        directory_file_store_service.data_config["dir_path"],
        directory_file_store_service.tenant_service.tenant.slug,
        directory_file_store_service.data_config["media"]["dir_path"]))
    return base_path


async def test_directory_file_store_service_store(
        directory_file_store_service, base_path, encoded_image):
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"
    data_type = 'images'

    content = encoded_image
    contexts = [{
        'id': id_,
        'created_at': 1583964551,
        'type': data_type,
        'extension': extension,
        'content': content
    }]

    uri, *_ = await directory_file_store_service.store(contexts)

    image_path = base_path / uri
    assert image_path.is_file()
    assert uri == "images/2020/03/11/abca8e11-0719-44ab-bd3f-ed5aa1bd2918.png"


async def test_directory_file_store_service_store_many(
        directory_file_store_service, base_path, encoded_image):
    contexts = [
        {
            'id': "abca8e11-0719-44ab-bd3f-ed5aa1bd2918",
            'created_at': 1583964551,
            'type': 'images',
            'extension': "png",
            'content': encoded_image
        },
        {
            'id': "c41cc73c-b252-4072-82e2-0f5c081d9f4c",
            'created_at': 1583964551,
            'type': 'images',
            'extension': "png",
            'content': encoded_image
        }
    ]

    uris = await directory_file_store_service.store(contexts)
    for uri in uris:
        image_path = base_path / uri
        assert image_path.is_file()

    assert uris[0] == (
        "images/2020/03/11/abca8e11-0719-44ab-bd3f-ed5aa1bd2918.png")
    assert uris[1] == (
        "images/2020/03/11/c41cc73c-b252-4072-82e2-0f5c081d9f4c.png")


async def test_directory_file_store_service_load(
        directory_file_store_service, base_path, encoded_image):
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"
    data_type = 'images'

    content = encoded_image
    contexts = [{
        'id': id_,
        'created_at': 1583964551,
        'type': data_type,
        'extension': extension,
        'content': content
    }]

    uri, *_ = await directory_file_store_service.store(contexts)

    content, context = await directory_file_store_service.load(uri)

    assert content == b64decode(encoded_image)
    assert context == {
        'status': 200,
        'headers': {}
    }
