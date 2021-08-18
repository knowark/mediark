from mediark.application.general.suppliers import (
    EmailSupplier, MemoryEmailSupplier)


def test_email_supplier_methods() -> None:
    methods = EmailSupplier.__abstractmethods__  # type: ignore
    assert 'send' in methods

async def test_memory_email_suplier_process() -> None:
    email_supplier = MemoryEmailSupplier()

    payload = [{
                    "id": "E001",
                    "template": "mail/auth/activation.html",
                    "context": {
                        "type": "activation",
                        "subject": "New Account Activation",
                        "recipient": "valenep@example.com",
                        "owner": "Valentina",
                        "token": "<verification_token>"
                    }
                }]

    await email_supplier.send(payload)

    assert email_supplier._send == True
