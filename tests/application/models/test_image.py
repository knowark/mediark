from mediark.application.models import Image


def test_image_instantiation():
    image = Image()
    assert image is not None
