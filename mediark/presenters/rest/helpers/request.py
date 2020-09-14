from typing import Tuple, List, Dict, Any
from aiohttp import web
from .format import parse_domain, parse_dict
from json import JSONDecodeError, loads


async def get_request_filter(request: web.Request) -> Tuple:
    filter = request.query.get('filter')
    limit = int(request.query.get('limit') or 1000)
    offset = int(request.query.get('offset') or 0)

    query = {}
    try:
        query = loads(await request.text())
    except JSONDecodeError:
        pass

    domain = parse_domain(query.get('filter', filter))

    return domain, query.get('limit', limit), query.get('offset', offset)


async def get_request_ids(request: web.Request) -> List[str]:
    ids = []
    uri_id = request.match_info.get('id')
    if uri_id:
        ids.append(uri_id)

    body = await request.text()
    if body:
        ids.extend(loads(await request.text()))

    return ids


async def missing(value: Any) -> None:
    raise ValueError('Not implemented endpoint.')

# def get_request_filter(request: web.Request) -> Tuple:
#     parameters = get_parameters(request)
#     filter: str = parameters.get('filter', "")
#     limit: int = int(parameters.get('limit', 1000))
#     offset: int = int(parameters.get('offset', 0))

#     domain = parse_domain(filter)

#     return domain, limit, offset


# def get_parameters(request: web.Request) -> Dict[str, Any]:
#     return parse_dict(request.query)
