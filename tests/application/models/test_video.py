from mediark.application.models import Video


def test_video_instantiation():
    video = Video()
    assert video is not None
