from json import loads
from aiohttp import web
from injectark import Injectark
from typing import Callable, Type, Tuple, Dict
from validark import normalize,  validate
from ..helpers import get_request_filter, get_request_ids
from .operations import operations


class Resource:
    def __init__(self, spec: dict, injector: Injectark) -> None:
        self.spec = spec
        self.injector = injector
        self.paths = self.spec['paths']

    async def head(self, request) -> web.Response:
        domain, _, _ = await get_request_filter(request)
        resource = request.match_info['resource']
        path = self.paths[f'/{resource}']['head']
        action = 'default'

        handler, fixed_meta = self.resolve_operation(
            path['operationId'], action)

        meta = {'domain': domain}
        meta.update(fixed_meta)

        result = await handler({'meta': meta})

        return web.json_response(
            {'data': None}, headers={'Count': str(result['data'])})

    async def get(self, request: web.Request) -> web.Response:
        domain, limit, offset = await get_request_filter(request)
        action = 'default'

        resource = request.match_info['resource']
        path = self.paths[f'/{resource}']['get']

        handler, fixed_meta = self.resolve_operation(
            path['operationId'], action)

        meta = {'domain': domain, 'limit': limit, 'offset': offset}
        meta.update(fixed_meta)
        result = await handler({'meta': meta})
        return web.json_response(normalize(result))

    async def patch(self, request: web.Request) -> web.Response:
        entry = loads(await request.text())
        action = entry.get('meta', {}).get('action','default')

        resource = request.match_info['resource']
        path = self.paths[f'/{resource}']['patch']

        handler, fixed_meta = self.resolve_operation(
            path['operationId'], action)

        entry.setdefault('meta', {}).update(fixed_meta)
        result = await handler(normalize(entry, 'snake'))

        return web.json_response(normalize(result))


    def resolve_operation(
        self, operationId: str, action: str) -> Tuple[Callable, Dict]:
        operation_map = operations()[operationId]

        route = operation_map['actions'][action]

        class_name, method_name = route['handler'].split('.')
        meta = route['meta']

        return getattr(self.injector[class_name], method_name),meta

