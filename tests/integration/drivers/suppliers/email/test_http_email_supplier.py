import os
from pytest import fixture
from time import gmtime, strftime
from mediark.integration.drivers.suppliers import HttpEmailSupplier
from mediark.integration.drivers.suppliers.email import (
     http_email_supplier as http_email_supplier_module)
#from mediark.integration.drivers.suppliers.email import smtplib

@fixture
def http_email_supplier(monkeypatch):
    return HttpEmailSupplier({
        "sender": "mediark@tempos.site",
        "host": "smtp.dreamhost.com",
        "port": "465",
        "username": "mediark@tempos.site",
        "password": "jV4yY?Q9",
     })

async def test_http_email_supplier_instantiation(
    http_email_supplier) -> None:
    assert http_email_supplier is not None

async def xtest_http_email_supplier_process(
        http_email_supplier, monkeypatch):



    arguments = {}
    def mock_run(sender, recipient, message):
         nonlocal arguments
         arguments['sender'] = sender
         arguments['recipient'] = recipient
         arguments['message'] = message

    monkeypatch.setattr(
        http_email_supplier_module, 'sendmail', mock_run)

    payload = {
        "recipient": "info@example.com",
        "context": "Prueba"
    }

    await http_email_supplier.send(payload)

    assert arguments == {
        "sender": "mediark@tempos.site",
        "recipient": "info@example.com",
        "message": "Prueba"
    }

