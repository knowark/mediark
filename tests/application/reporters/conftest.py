from pytest import fixture
from injectark import Injectark
from mediark.application.models import Media, Image, Audio
from mediark.application.repositories import (
    MemoryMediaRepository, MemoryImageRepository, MemoryAudioRepository)
from mediark.application.utilities import (
    Tenant, StandardTenantProvider, StandardTenantProvider,
    StandardAuthProvider, QueryParser)
from mediark.application.services import MemoryFileStoreService
from mediark.application.reporters import (
    MediarkReporter, StandardMediarkReporter,
    FileReporter, StandardFileReporter)


@fixture
def media_repository():
    parser = QueryParser()
    auth_provider = StandardAuthProvider()
    tenant_service = StandardTenantProvider()
    media_repository = MemoryMediaRepository(
        parser, tenant_service, auth_provider)
    media_repository.load({
        'default': {
            '001': Media(id='001', reference='ABC'),
            '002': Media(id='002', reference='XYZ')
        }
    })
    return media_repository


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
def mediark_reporter(media_repository, image_repository, audio_repository):
    return StandardMediarkReporter(media_repository,
                                   image_repository, audio_repository)


@fixture
def file_reporter():
    file_store_service = MemoryFileStoreService(
        StandardTenantProvider(),
        StandardAuthProvider())
    return StandardFileReporter(file_store_service)
