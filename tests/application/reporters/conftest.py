from pytest import fixture
from mediark.application.models import Image
from mediark.application.repositories import (
    ExpressionParser, MemoryImageRepository)
from mediark.application.reporters import (
    MediarkReporter, MemoryMediarkReporter)


@fixture
def image_repository():
    parser = ExpressionParser()
    image_repository = MemoryImageRepository(parser)
    image_repository.load({
        '001': Image(id='001', reference='ABC'),
        '002': Image(id='002', reference='XYZ')
    })
    return image_repository


@fixture
def mediark_reporter(image_repository):
    return MemoryMediarkReporter(image_repository)
