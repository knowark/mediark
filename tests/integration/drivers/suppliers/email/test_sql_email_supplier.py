import os
from pytest import fixture
from time import gmtime, strftime
from mediark.integration.drivers.suppliers import SqlEmailSupplier
from mediark.integration.drivers.suppliers.email import (
     sql_email_supplier as sql_email_supplier_module)


@fixture
def sql_email_supplier(monkeypatch):
    return SqlEmailSupplier({

        "sender": "",
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "url": "",
        "path": ""
     })

async def test_sql_email_supplier_instantiation(
    sql_email_supplier) -> None:
    assert sql_email_supplier is not None

async def test_sql_email_supplier_process(
        sql_email_supplier, monkeypatch):
    pass
