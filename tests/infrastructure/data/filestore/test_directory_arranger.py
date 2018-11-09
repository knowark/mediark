from pathlib import Path
from pytest import fixture, raises
from mediark.infrastructure.data import (FilestoreArranger)


def test_filestore_arranger_instantiation_imagen(filestore_arranger_image):
    assert isinstance(filestore_arranger_image, FilestoreArranger)
    assert filestore_arranger_image.extension == 'png'


# def test_filestore_arranger_instantiation_audio(filestore_arranger_audio):
#     assert isinstance(filestore_arranger_audio, FilestoreManager)
#     assert filestore_arranger_audio.extension == 'mp3'


# def test_filestore_arranger_create_directory_structure_image(
#         filestore_arranger_image):
#     hex_digits = list('0123456789abcdef')
#     base_dir = Path(filestore_arranger_image.base_path)

#     subdirs = [str(x) for x in base_dir.iterdir() if x.is_dir()]

#     for i in hex_digits:
#         for j in hex_digits:
#             hex_dir = str(base_dir.joinpath(i + j))
#             assert hex_dir in subdirs


# def test_filestore_arranger_create_directory_structure_audio(
#         filestore_arranger_audio):
#     hex_digits = list('0123456789abcdef')
#     base_dir = Path(filestore_arranger_audio.base_path)

#     subdirs = [str(x) for x in base_dir.iterdir() if x.is_dir()]

#     for i in hex_digits:
#         for j in hex_digits:
#             hex_dir = str(base_dir.joinpath(i + j))
#             assert hex_dir in subdirs


# def test_filestore_arranger_create_nested_directory_structure_image(
#         filestore_arranger_image):
#     hex_digits = list('0123456789abcdef')
#     base_dir = Path(filestore_arranger_image.base_path)

#     root_dirs = [x for x in base_dir.iterdir() if x.is_dir()]

#     for root_hex_dir in root_dirs:
#         subdirs = [str(x) for x in root_hex_dir.iterdir() if x.is_dir()]
#         for i in hex_digits:
#             for j in hex_digits:
#                 hex_dir = str(root_hex_dir.joinpath(i + j))
#                 assert hex_dir in subdirs


# def test_filestore_arranger_create_nested_directory_structure_audio(
#         filestore_arranger_audio):
#     hex_digits = list('0123456789abcdef')
#     base_dir = Path(filestore_arranger_audio.base_path)

#     root_dirs = [x for x in base_dir.iterdir() if x.is_dir()]

#     for root_hex_dir in root_dirs:
#         subdirs = [str(x) for x in root_hex_dir.iterdir() if x.is_dir()]
#         for i in hex_digits:
#             for j in hex_digits:
#                 hex_dir = str(root_hex_dir.joinpath(i + j))
#                 assert hex_dir in subdirs


# def test_filestore_arranger_save_image(filestore_arranger_image, base64_image):
#     id_ = "8d938e11-0719-44ab-bd3f-ed5aa1bd2918"
#     extension = "png"
#     image_path = Path(filestore_arranger_image.base_path).joinpath(
#         "8d", "93", "{0}.{1}".format(id_, extension))

#     uri = filestore_arranger_image.save(id_, base64_image)
#     assert image_path.is_file()
#     assert uri == "8d/93/8d938e11-0719-44ab-bd3f-ed5aa1bd2918.png"


# def test_filestore_arranger_save_audio(filestore_arranger_audio, base64_audio):
#     id_ = "8d938e11-0719-44ab-bd3f-ed5aa1bd2918"
#     extension = "mp3"
#     audio_path = Path(filestore_arranger_audio.base_path).joinpath(
#         "8d", "93", "{0}.{1}".format(id_, extension))

#     uri = filestore_arranger_audio.save(id_, base64_audio)

#     assert audio_path.is_file()
#     assert uri == "8d/93/8d938e11-0719-44ab-bd3f-ed5aa1bd2918.mp3"


# def test_filestore_arranger_get_subdirs_too_short_id_image(
#         filestore_arranger_image):
#     with raises(ValueError):
#         filestore_arranger_image._get_subdirs("NOT")


# def test_filestore_arranger_get_subdirs_too_short_id_audio(
#         filestore_arranger_audio):
#     with raises(ValueError):
#         filestore_arranger_audio._get_subdirs("NOT")
