from mediark.application.general.suppliers import (
    EmailSupplier, MemoryEmailSupplier)


def test_email_supplier_methods() -> None:
    methods = EmailSupplier.__abstractmethods__  # type: ignore
    assert 'process' in methods

async def test_memory_email_suplier_process() -> None:
    email_supplier = MemoryEmailSupplier()

    email = {
            'email_to': 'info@example.com',
            'title': 'Envio Directo',
            'body': 'Mensaje directo sin abstracción'
        }
    tenant = "knowark"

    await email_supplier.process(tenant, email)

    assert email_supplier._process == True
