from mediark.application.models import Image


def test_image_instantiation():
    image = Image()

    assert image.id == ''
    assert image.namespace == ''
    assert image.reference == ''
    assert image.extension == 'jpg'
    assert image.uri == ''


def test_image_attributes():
    image = Image(id='63b0e6ff-42b9-444d-9a3a-483564b493bc',
                  namespace='https://example.com',
                  reference='00648c29-eca2-4112-8a1a-4deedb443188',
                  extension='png',
                  uri=('https://mediark.knowark.com/media/images/'
                       '00648c29-eca2-4112-8a1a-4deedb443188.png'))

    assert image.id == '63b0e6ff-42b9-444d-9a3a-483564b493bc'
    assert image.namespace == 'https://example.com'
    assert image.reference == '00648c29-eca2-4112-8a1a-4deedb443188'
    assert image.extension == 'png'
    assert image.uri == ('https://mediark.knowark.com/media/images/'
                         '00648c29-eca2-4112-8a1a-4deedb443188.png')
