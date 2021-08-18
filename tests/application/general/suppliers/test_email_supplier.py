from mediark.application.general.suppliers import (
    EmailSupplier, MemoryEmailSupplier)


def test_email_supplier_methods() -> None:
    methods = EmailSupplier.__abstractmethods__  # type: ignore
    assert 'send' in methods

async def test_memory_email_suplier_process() -> None:
    email_supplier = MemoryEmailSupplier()

    payload = {
            'recipient': 'info@example.com',
            'conext': 'Envio Directo'
        }

    await email_supplier.send(payload)

    assert email_supplier._send == True
