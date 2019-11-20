from mediark.application.reporters import MediarkReporter
from .conftest import *

def test_mediark_reporter_instantiation(mediark_reporter):
    assert isinstance(mediark_reporter, MediarkReporter)


def test_mediark_reporter_search_images(mediark_reporter):
    result = mediark_reporter.search_images([])
    assert len(result) == 2


def test_mediark_reporter_search_audios(mediark_reporter):
    result = mediark_reporter.search_audios([])
    assert len(result) == 2
