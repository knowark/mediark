import os
import ssl
from pytest import fixture
from time import gmtime, strftime
from unittest.mock import MagicMock, AsyncMock
from mediark.integration.drivers.suppliers import HttpEmailSupplier
from mediark.integration.drivers.suppliers.email import (
     http_email_supplier as http_email_supplier_module)
from mediark.integration.drivers.suppliers.email.http_email_supplier import smtplib


@fixture
def http_email_supplier(monkeypatch):
    return HttpEmailSupplier({
        "sender": "mediark@tempos.site",
        "host": "smtp.dreamhost.com",
        "port": "465",
        "username": "mediark@tempos.site",
        "password": "jV4yY?Q9",
        "path": "/opt/mediark/templates/tempos_templates/"
     })


async def test_http_email_supplier_instantiation(
    http_email_supplier) -> None:
    assert http_email_supplier is not None


async def test_http_email_supplier_process(
        http_email_supplier, monkeypatch):

    class MockSMTP_SSL(MagicMock(smtplib.SMTP_SSL, autospec=True)):
        def __enter__(self):
            return MagicMock(smtplib.SMTP_SSL)

        def __exit__(self, *_):
            pass


    monkeypatch.setattr(
        smtplib, 'SMTP_SSL', MockSMTP_SSL)


    payload = [{
                    "id": "E001",
                    "template": "mail/auth/registered.html",
                    "context": {
                        "type": "registered",
                        "user_name": "Pepe Perez",
                        "shop_url": "tempos.site",
                        "unsubscribe_link": "tempos.site",
                        "subject": "Nuevo Registro",
                        "recipient": "valenep@example.com",
                        "owner": "Valentina"
                    }
                }]
    await http_email_supplier.send(payload)

    call_args_list = http_email_supplier.smtp.SMTP_SSL.call_args
    assert call_args_list.args[0] == "smtp.dreamhost.com"
    assert call_args_list.args[1] == "465"
    assert isinstance(call_args_list.kwargs['context'], ssl.SSLContext)
