# from pytest import raises
# from pathlib import Path


# def test_directory_file_store_service(
#         directory_file_store_service, base64_image):
#     id_ = "abca8e11-0719-44ab-bd3f-ed5aa1bd2918"
#     extension = "png"
#     image_path = Path(directory_file_store_service.base_path).joinpath(
#         "ab", "ca", "{0}.{1}".format(id_, extension))

#     uri = directory_file_store_service.store(id_, base64_image)
#     assert image_path.is_file()
#     assert uri == "ab/ca/abca8e11-0719-44ab-bd3f-ed5aa1bd2918.png"


# def test_filestore_manager_get_subdirs_too_short_id_image(
#         directory_file_store_service):
#     with raises(ValueError):
#         directory_file_store_service._get_subdirs("NOT")
