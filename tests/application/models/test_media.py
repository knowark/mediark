from mediark.application.models import Media


def test_media_instantiation():
    media = Media()

    assert media.id == ''
    assert media.name == ''
    assert media.type == 'general'
    assert media.namespace == ''
    assert media.reference == ''
    assert media.extension == 'jpg'
    assert media.uri == ''


def test_media_attributes():
    media = Media(id='63b0e6ff-42b9-444d-9a3a-483564b493bc',
                  name='knowark_logo',
                  type='images',
                  namespace='https://example.com',
                  reference='00648c29-eca2-4112-8a1a-4deedb443188',
                  extension='png',
                  uri=('https://mediark.knowark.com/media/medias/'
                       '00648c29-eca2-4112-8a1a-4deedb443188.png'))

    assert media.id == '63b0e6ff-42b9-444d-9a3a-483564b493bc'
    assert media.name == 'knowark_logo'
    assert media.type == 'images'
    assert media.namespace == 'https://example.com'
    assert media.reference == '00648c29-eca2-4112-8a1a-4deedb443188'
    assert media.extension == 'png'
    assert media.uri == ('https://mediark.knowark.com/media/medias/'
                         '00648c29-eca2-4112-8a1a-4deedb443188.png')
