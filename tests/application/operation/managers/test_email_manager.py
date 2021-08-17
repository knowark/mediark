from pytest import fixture
from mediark.application.domain.common import (
    QueryParser, DataDict, DataValidationError,
    StandardTenantProvider, Tenant, RecordList,
    StandardAuthProvider, User)
from mediark.application.general.suppliers import EmailSupplier
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
def email_manager() -> EmailManager:
    return EmailManager(email_supplier)

def test_email_manager_instantiation(email_manager) -> None:
    assert hasattr(email_manager, 'process')

async def test_email_manager_process(
    email_manager: EmailManager) -> None:

    payload = {
            'email_to': 'info@example.com',
            'title': 'Envio Directo',
            'body': 'Mensaje directo sin abstracción'
        }


    await email_manager.process({
                "data": payload,
                "meta":{
                    "tenant": "knowark"
                }
            })

