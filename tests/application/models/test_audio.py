from mediark.application.models import Audio


def test_audio_instantiation():
    audio = Audio()
    assert audio is not None
