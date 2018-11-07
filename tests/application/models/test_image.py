from mediark.application.models import Image


def test_image_instantiation():
    image = Image()

    assert image.namespace == ''
    assert image.reference == ''
    assert image.extension == 'jpg'
    assert image.url == ''


def test_image_attributes():
    image = Image(namespace='https://example.com',
                  reference='00648c29-eca2-4112-8a1a-4deedb443188',
                  extension='png',
                  url=('https://mediark.knowark.com/media/images/'
                       '00648c29-eca2-4112-8a1a-4deedb443188.png'))

    assert image.namespace == 'https://example.com'
    assert image.reference == '00648c29-eca2-4112-8a1a-4deedb443188'
    assert image.extension == 'png'
    assert image.url == ('https://mediark.knowark.com/media/images/'
                         '00648c29-eca2-4112-8a1a-4deedb443188.png')
