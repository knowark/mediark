from mediark.application.reporters import MediarkReporter
from .conftest import *


def test_mediark_reporter_instantiation(mediark_reporter):
    assert isinstance(mediark_reporter, MediarkReporter)


async def test_mediark_reporter_search_media(mediark_reporter):
    result = await mediark_reporter.search_media([])
    assert len(result) == 2
