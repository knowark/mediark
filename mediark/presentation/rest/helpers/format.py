import re
from json import loads, JSONDecodeError
from typing import Tuple, List, Dict, Any
from validark import camel_to_snake


def parse_domain(filter: str) -> List[Any]:
    domain: List[Any] = []
    try:
        domain = loads(filter or "")
    except JSONDecodeError:
        return domain

    for item in domain:
        if isinstance(item, list) and len(item):
            word = camel_to_snake(item[0])
            item[0] = word

    return domain
