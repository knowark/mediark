from pytest import fixture
from mediark.application.models import Image, Audio
from mediark.application.repositories import (
    MemoryImageRepository, MemoryAudioRepository)
from mediark.application.utilities.expression_parser import ExpressionParser
from mediark.application.reporters import (
    MediarkReporter, StandardMediarkReporter)


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
def audio_repository():
    parser = ExpressionParser()
    audio_repository = MemoryAudioRepository(parser)
    audio_repository.load({
        '001': Audio(id='001', reference='ABC'),
        '002': Audio(id='002', reference='XYZ')
    })
    return audio_repository


@fixture
def mediark_reporter(image_repository, audio_repository):
    return StandardMediarkReporter(image_repository, audio_repository)
