from json import loads, decoder
from typing import Tuple, List, Any
from flask import Request


def get_request_filter(request: Request) -> Tuple:
    domain: List[Any] = []
    filter = request.args.get('filter')
    limit = int(request.args.get('limit') or 0)
    offset = int(request.args.get('offset') or 0)

    if filter:
        try:
            domain = loads(filter)
        except decoder.JSONDecodeError:
            pass

    return domain, limit, offset
