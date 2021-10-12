from mediark.application.general.suppliers import (
    EmailSupplier, MemoryEmailSupplier)


def test_email_supplier_methods() -> None:
    methods = EmailSupplier.__abstractmethods__  # type: ignore
    assert 'send' in methods

async def test_memory_email_suplier_process() -> None:
    email_supplier = MemoryEmailSupplier()

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

    await email_supplier.send(payload)

    assert email_supplier._send == True
