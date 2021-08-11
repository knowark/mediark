from typing import Tuple, List, Dict, Any
from aiohttp import web
from .format import parse_domain
from json import JSONDecodeError, loads


async def get_request_filter(request: web.Request) -> Tuple:
    filter = request.query.get('filter')
    limit = int(request.query.get('limit') or 1000)
    offset = int(request.query.get('offset') or 0)
    print("ENTRA AL  FILTER>>>"*50)
    print(filter)
    query = {}
    try:
        query = loads(await request.text())
    except JSONDecodeError:
        pass

    domain = parse_domain(query.get('filter', filter))
    print(domain)
    return domain, query.get('limit', limit), query.get('offset', offset)


async def get_request_ids(request: web.Request) -> List[str]:
    print("ENTRA GET REQUEST IDS>>>>"*50)
    print(request)
    ids = []
    uri_id = request.match_info.get('id')
    print(uri_id)
    if uri_id:
        ids.append(uri_id)
    print(ids)
    body = await request.text()
    print(body)
    if body:
       print("ENTRA AL BODY>>>"*50)
       ids.extend(loads(await request.text())['data'])

    return ids
