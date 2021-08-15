from mediark.application.domain.models import Media


def test_media_instantiation():
    media = Media()

    assert media.id != ''
    assert media.name == ''
    assert media.type == ''
    assert media.reference == ''
    assert media.uri == ''


def test_media_attributes():
    media = Media(id='63b0e6ff-42b9-444d-9a3a-483564b493bc',
                  name='knowark_logo',
                  type='image/png',
                  reference='00648c29-eca2-4112-8a1a-4deedb443188',
                  uri=('https://mediark.knowark.com/media/medias/'
                       '00648c29-eca2-4112-8a1a-4deedb443188.png'))

    assert media.id == '63b0e6ff-42b9-444d-9a3a-483564b493bc'
    assert media.name == 'knowark_logo'
    assert media.type == 'image/png'
    assert media.reference == '00648c29-eca2-4112-8a1a-4deedb443188'
    assert media.uri == ('https://mediark.knowark.com/media/medias/'
                         '00648c29-eca2-4112-8a1a-4deedb443188.png')
