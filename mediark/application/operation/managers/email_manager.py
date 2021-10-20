import jwt
from datetime import datetime
from ...domain.services import EmailRepository
from ...domain.common import (TenantProvider, AuthProvider)
from ...general.suppliers import (
    EmailSupplier, PlanSupplier)


class EmailManager:
    def __init__(self, config: dict,  email_supplier: EmailSupplier,
                 email_repository: EmailRepository,
                 plan_supplier: PlanSupplier,
                 tenant_provider: TenantProvider,
                 auth_provider: AuthProvider) -> None:
        self.path = config['path']
        self.email_supplier = email_supplier
        self.email_repository = email_repository
        self.plan_supplier = plan_supplier
        self.tenant_provider = tenant_provider
        self.auth_provider = auth_provider


    async def request(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']
        tenant = self.tenant_provider.tenant.name
        tenant_id = self.tenant_provider.tenant.id
        user = self.auth_provider.user.name
        user_id = self.auth_provider.user.id
        user_email = self.auth_provider.user.email

        items = await self.email_repository.find(data, init=True)
        for record, item in zip(data, items):
            item.transition(record)

        result = [vars(item) for item in
                  await self.email_repository.add(items)]

        user_dict = {
                 "tid": tenant_id,
                 "uid": user_id,
                 "tenant": tenant,
                 "name": user,
                 "email": user_email,
                 "exp": int(datetime.now().timestamp()) + 604800
        }
        token = jwt.encode(user_dict, "", algorithm="HS256").decode('utf-8')

        for item in result:
            await self.plan_supplier.defer("SendEmailJob", {
                "meta": {
                    "authorization": token
                },
                "data":{
                    "email_id": item['id']}
            })

        return {'data': [item for item in result]}

    async def send(self, entry: dict) -> dict:
        meta, data = entry['meta'], entry['data']

        emails = [vars(item) for item in
                    await self.email_repository.search(
                        [('id', '=', data['email_id'])])]

        await self.email_supplier.send(emails)
        return {"data": emails}
