from mediark.application.models import Audio


def test_audio_instantiation():
    audio = Audio()

    assert audio.id == ''
    assert audio.namespace == ''
    assert audio.reference == ''
    assert audio.extension == 'mp3'
    assert audio.uri == ''


def test_audio_attributes():
    audio = Audio(id='63b0e6ff-42b9-444d-9a3a-483564b493bc',
                  namespace='https://example.com',
                  reference='00648c29-eca2-4112-8a1a-4deedb443188',
                  extension='png',
                  uri=('https://mediark.knowark.com/media/audios/'
                       '00648c29-eca2-4112-8a1a-4deedb443188.png'))

    assert audio.id == '63b0e6ff-42b9-444d-9a3a-483564b493bc'
    assert audio.namespace == 'https://example.com'
    assert audio.reference == '00648c29-eca2-4112-8a1a-4deedb443188'
    assert audio.extension == 'png'
    assert audio.uri == ('https://mediark.knowark.com/media/audios/'
                         '00648c29-eca2-4112-8a1a-4deedb443188.png')
