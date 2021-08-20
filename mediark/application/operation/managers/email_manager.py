from ...domain.services import EmailRepository
from ...general.suppliers import EmailSupplier


class EmailManager:
    def __init__(self, config: dict,  email_supplier: EmailSupplier,
                 email_repository: EmailRepository) -> None:
        self.path = config['path']
        self.email_supplier = email_supplier
        self.email_repository = email_repository

    async def send(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        items = await self.email_repository.find(data, init=True)
        for record, item in zip(data, items):
            item.transition(record)

        result = [vars(item) for item in await self.email_repository.add(items)]
        await self.email_supplier.send(result)
        return {"data": "Email send successfully"}
