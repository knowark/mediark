from pytest import fixture
from mediark.application.domain.common import (
    QueryParser, DataDict, DataValidationError,
    StandardTenantProvider, Tenant, RecordList,
    StandardAuthProvider, User)
from mediark.application.domain.services.repositories import (
    RepositoryService, EmailRepository, MemoryEmailRepository)
from mediark.application.general.suppliers import (
    EmailSupplier, MemoryEmailSupplier, PlanSupplier, MemoryPlanSupplier)
from mediark.application.operation.managers import EmailManager


# parser

@fixture
def parser() -> QueryParser:
    return QueryParser()


# providers

@fixture
def auth_provider() -> StandardAuthProvider:
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name='johndoe'))
    return auth_provider


@fixture
def tenant_provider() -> StandardTenantProvider:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Default"))
    return tenant_provider

# repositories

@fixture
def email_repository(tenant_provider, auth_provider):
    return MemoryEmailRepository(
        QueryParser(), tenant_provider, auth_provider)


@fixture
def email_supplier() -> EmailSupplier:
    return MemoryEmailSupplier()

@fixture
def plan_supplier() -> PlanSupplier:
    return MemoryPlanSupplier()


@fixture
def email_manager(email_supplier, email_repository,
                  plan_supplier, tenant_provider,
                  auth_provider) -> EmailManager:
    return EmailManager({"path": "/opt/mediark/templates/"},
                        email_supplier, email_repository,
                        plan_supplier, tenant_provider, auth_provider)


def test_email_manager_instantiation(email_manager) -> None:
    assert hasattr(email_manager, 'send')

async def test_email_manager_request(
    email_manager: EmailManager) -> None:

    payload:RecordList = [{
        "id": "001",
        "template": "mail/auth/registered.html",
        "recipient": "info@example.com",
        "subject": "New Registered",
        "type": "registered",
        "context": {
            "user_name": "Info",
            "shop_url": "https://www.tempos.site",
            "unsubscribe_link": "https://www.tempos.site"
            }
        }]

    items = getattr(
          email_manager.email_repository, 'data')['default']

    assert len(items) == 0

    result = await email_manager.request({
                "data": payload,
                "meta":{}
            })

    assert result['data'][0]['id'] == "001"
    assert len(items)==1


async def test_email_manager_send(
    email_manager: EmailManager) -> None:

    payload:RecordList = [{
        "id": "001",
        "template": "mail/auth/registered.html",
        "recipient": "info@example.com",
        "subject": "New Registered",
        "type": "registered",
        "context": {
            "user_name": "Info",
            "shop_url": "https://www.tempos.site",
            "unsubscribe_link": "https://www.tempos.site"
            }
        }]

    result = await email_manager.request({
                "data": payload,
                "meta":{}
            })


    payload = {
        'email_id': '001'
    }

    await email_manager.send({
                "data": payload,
                "meta":{}
            })

    assert email_manager.email_supplier._send is True
