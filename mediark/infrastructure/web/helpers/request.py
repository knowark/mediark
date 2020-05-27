from json import JSONDecodeError, loads
from typing import Tuple, Dict, Any
from aiohttp import web
from .format import parse_domain, parse_dict


async def get_request_filter(request: web.Request) -> Tuple:
    parameters = get_parameters(request)
    filter: str = parameters.get('filter', "")
    limit: int = int(parameters.get('limit', 10_000))
    offset: int = int(parameters.get('offset', 0))

    query = {}
    try:
        query = loads(await request.text())
    except JSONDecodeError:
        pass

    domain = parse_domain(query.get('filter', filter))

    return domain, query.get('limit', limit), query.get('offset', offset)

def get_parameters(request: web.Request) -> Dict[str, Any]:
    return parse_dict(request.query)
