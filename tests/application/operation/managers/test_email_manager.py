from pytest import fixture
from mediark.application.domain.common import (
    QueryParser, DataDict, DataValidationError,
    StandardTenantProvider, Tenant, RecordList,
    StandardAuthProvider, User)
from mediark.application.general.suppliers import (EmailSupplier,
                                                   MemoryEmailSupplier)
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


@fixture
def email_supplier() -> EmailSupplier:
    return MemoryEmailSupplier()


@fixture
def email_manager(email_supplier) -> EmailManager:
    return EmailManager(email_supplier)


def test_email_manager_instantiation(email_manager) -> None:
    assert hasattr(email_manager, 'send')

async def test_email_manager_send(
    email_manager: EmailManager) -> None:

    payload = {
            'recipient': 'info@example.com',
            'context': 'Envio Directo'
        }


    await email_manager.send({
                "data": payload,
                "meta":{
                }
            })

