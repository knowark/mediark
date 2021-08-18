from ...domain.services import RepositoryService
from ...general.suppliers import EmailSupplier


class EmailManager:
    def __init__(self, config: dict,  email_supplier: EmailSupplier,
                 repository_service: RepositoryService) -> None:
        self.path = config['path']
        self.email_supplier = email_supplier
        self.repository_service = repository_service

    async def send(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        repository = self.repository_service.resolve(meta.pop('model'))


        items = await repository.find(data, init=True)
        for record, item in zip(data, items):
            item.transition(record)

        result = [vars(item) for item in await repository.add(items)]

        await self.email_supplier.send(result)
        return {"data": "Email send successfully"}
