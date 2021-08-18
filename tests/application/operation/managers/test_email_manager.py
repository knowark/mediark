from pytest import fixture
from mediark.application.domain.common import (
    QueryParser, DataDict, DataValidationError,
    StandardTenantProvider, Tenant, RecordList,
    StandardAuthProvider, User)
from mediark.application.domain.services.repositories import (
    RepositoryService, EmailRepository, MemoryEmailRepository)
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

# repositories

@fixture
def email_repository(tenant_provider, auth_provider):
    return MemoryEmailRepository(
        QueryParser(), tenant_provider, auth_provider)

@fixture
def repository_service(email_repository):
    return RepositoryService([email_repository])


@fixture
def email_supplier() -> EmailSupplier:
    return MemoryEmailSupplier()


@fixture
def email_manager(email_supplier, repository_service) -> EmailManager:
    return EmailManager({
        "path": "/opt/mediark/templates/"
    },
    email_supplier, repository_service)


def test_email_manager_instantiation(email_manager) -> None:
    assert hasattr(email_manager, 'send')

async def test_email_manager_send(
    email_manager: EmailManager) -> None:

    payload = [{
        "template": "mail/auth/activation.html",
        "context": {
            "type": "activation",
            "subject": "New Account Activation",
            "recipient": "valenep@example.com",
            "owner": "Valentina",
            "token": "<verification_token>"
            }
        }]


    await email_manager.send({
                "data": payload,
                "meta":{
                    "model": "Email"
                }
            })

