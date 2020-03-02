from pytest import raises
from pathlib import Path


async def test_directory_file_store_service(
        directory_file_store_service, encoded_image):
    id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
    extension = "png"

    base_path = Path("{0}/{1}/{2}/{3}".format(
        directory_file_store_service.data_config["dir_path"],
        directory_file_store_service.tenant_service.tenant.slug,
        directory_file_store_service.data_config["media"]["dir_path"],
        directory_file_store_service.data_config[
            "media"][directory_file_store_service.data_type]["dir_path"]))

    image_path = base_path.joinpath(
        "ab", "ca", "{0}.{1}".format(id_, extension))

    uri = await directory_file_store_service.store(id_, encoded_image)
    assert image_path.is_file()
    assert uri == "ab/ca/abca8e11-0719-44ab-bd3f-ed5aa1bd2918.png"


def test_filestore_manager_get_subdirs_too_short_id_image(
        directory_file_store_service):
    with raises(ValueError):
        directory_file_store_service._get_subdirs("NOT")
