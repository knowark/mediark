from ...general.suppliers import EmailSupplier


class EmailManager:
    def __init__(self, email_supplier: EmailSupplier) -> None:
        self.email_supplier = email_supplier

    async def process(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        tenant = meta['tenant']
        await EmailSupplier.process(self, tenant, data)
        #await self.email_supplier.process(tenant, data)
        return {"data": "Email send successfully"}
