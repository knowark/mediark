from typing import List, Dict, Any
from .base import base
from .http import http
from .check import check
from .json import json
from .sql import sql
from .swift import swift


STRATEGIES = {
    'base': base,
    'http': http,
    'check': check,
    'json': json,
    'sql': sql,
    'swift': swift
}


def build_strategy(strategies: List[str],
                   custom_strategy: Dict[str, Any]=None) -> Dict[str, Any]:
    strategy: Dict[str, Any] = {}
    for name in strategies:
        strategy.update(STRATEGIES[name])
    strategy.update(custom_strategy)
    return strategy
