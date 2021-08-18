from ...general.suppliers import EmailSupplier


class EmailManager:
    def __init__(self, email_supplier: EmailSupplier) -> None:
        self.email_supplier = email_supplier

    async def send(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        await self.email_supplier.send(data)
        return {"data": "Email send successfully"}
