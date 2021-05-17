from typing import Any
from aiohttp import web
from injectark import Injectark
from ....core.http import HttpResponseWriter


class DownloadResource:
    def __init__(self, injector: Injectark) -> None:
        self.file_informer = injector['FileInformer']
        self.tenant_supplier = injector['TenantSupplier']
        self.session_manager = injector['SessionManager']

    async def get(self, request: web.Request) -> Any:
        tenant = request.match_info['tenant']
        path = request.match_info['path']

        tenant_dict = self.tenant_supplier.resolve_tenant(tenant)
        self.session_manager.set_tenant(tenant_dict)

        response = web.StreamResponse()
        response['request'] = request
        stream = HttpResponseWriter(response)

        await self.file_informer.load(path, stream)
