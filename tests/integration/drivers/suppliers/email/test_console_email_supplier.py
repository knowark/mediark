from pytest import fixture
from mediark.integration.drivers.suppliers import ConsoleEmailSupplier
from mediark.integration.drivers.suppliers.email import (
     console_email_supplier as console_email_supplier_module)


@fixture
def console_email_supplier(monkeypatch):
    return ConsoleEmailSupplier()


async def test_console_email_supplier_instantiation(
    console_email_supplier) -> None:
    assert console_email_supplier is not None


async def test_console_email_supplier_process(
        console_email_supplier, monkeypatch):

    payload = [{
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

    result =await console_email_supplier.send(payload)

    assert payload == result

