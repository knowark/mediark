from typing import Tuple, List, Dict, Any
from aiohttp import web
from .format import parse_domain, parse_dict


def get_request_filter(request: web.Request) -> Tuple:
    parameters = get_parameters(request)
    filter: str = parameters.get('filter', "")
    limit: int = int(parameters.get('limit', 1000))
    offset: int = int(parameters.get('offset', 0))

    domain = parse_domain(filter)

    return domain, limit, offset


def get_parameters(request: web.Request) -> Dict[str, Any]:
    return parse_dict(request.query)
