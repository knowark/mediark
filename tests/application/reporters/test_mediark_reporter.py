from mediark.application.reporters import MediarkReporter


def test_mediark_reporter_instantiation(mediark_reporter):
    assert isinstance(mediark_reporter, MediarkReporter)


def test_mediark_reporter_search_images(mediark_reporter):
    result = mediark_reporter.search_images([])
    assert len(result) == 2
