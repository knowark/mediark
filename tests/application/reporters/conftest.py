from pytest import fixture
from injectark import Injectark
from mediark.application.models import Image, Audio
from mediark.application.repositories import (
    MemoryImageRepository, MemoryAudioRepository)
from mediark.application.utilities import (
    Tenant, StandardTenantProvider, StandardTenantProvider,
    StandardAuthProvider)
from mediark.application.utilities.query_parser import QueryParser
from mediark.application.reporters import (
    MediarkReporter, StandardMediarkReporter)


@fixture
def image_repository():
    parser = QueryParser()
    auth_provider = StandardAuthProvider()
    tenant_service = StandardTenantProvider()
    image_repository = MemoryImageRepository(
        parser, tenant_service, auth_provider)
    image_repository.load({
        'default': {
            '001': Image(id='001', reference='ABC'),
            '002': Image(id='002', reference='XYZ')
        }
    })
    return image_repository


@fixture
def audio_repository():
    parser = QueryParser()
    auth_provider = StandardAuthProvider()
    tenant_service = StandardTenantProvider()
    audio_repository = MemoryAudioRepository(
        parser, tenant_service, auth_provider)
    audio_repository.load({
        'default': {
            '001': Audio(id='001', reference='ABC'),
            '002': Audio(id='002', reference='XYZ')
        }
    })
    return audio_repository


@fixture
def mediark_reporter(image_repository, audio_repository):
    return StandardMediarkReporter(image_repository, audio_repository)
