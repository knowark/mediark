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
    payload = {
        "meta": {
            "authorization":  (
            #     "tid": "001",
            #     "uid": "001",
            #     "tenant": "Knowark",
            #     "name": "John Doe",
            #     "email": "john@doe.com"
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwMDEiLCJ1aWQiOi"
            "IwMDEiLCJ0ZW5hbnQiOiJLbm93YXJrIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1ha"
            "WwiOiJqb2huQGRvZS5jb20ifQ."
            "g1FpaSQ9y-ZPyc3GW4gxlen8oflJVVmdCxt36D7KsaE"
        )},
        'data': {'email_id': '001'}
    }

    task = Task(payload=payload)
    result =  await job(task)
    print("resturn result job>>>>",result)
    assert result == {}

    payload = {
        "meta": {
            "authorization":  ""
        },
        'data': {'email_id': '001'}
    }

    task = Task(payload=payload)
    result =  await job(task)

    assert result == {'error': 'DecodeError: Not enough segments'}
