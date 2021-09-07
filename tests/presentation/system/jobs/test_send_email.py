from pytest import fixture
from injectark import Injectark
from schedulark import Task
from mediark.integration.core import config
from mediark.integration.factories import factory_builder
from mediark.presentation.system.jobs import SendEmailJob


@fixture
def injector():
    config['factory'] = 'CheckFactory'
    factory = factory_builder.build(config)

    injector = Injectark(factory)
    return injector


def test_send_email_job_instantiation(injector):
    job = SendEmailJob(injector)

    assert job is not None


async def test_send_email_job_call(injector):
    job = SendEmailJob(injector)

    task = None  # TODO: task should be a simple dict.
    result = await job(task)

    assert result == None
