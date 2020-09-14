from typing import List, Dict, Any
from .base import base
from .http import http
from .check import check
from .sql import sql
from .swift import swift
from .directory import directory


STRATEGIES = {
    'base': base,
    'http': http,
    'check': check,
    'sql': sql,
    'swift': swift,
    'directory': directory
}


def build_strategy(strategies: List[str],
                   custom_strategy: Dict[str, Any]={}) -> Dict[str, Any]:
    strategy: Dict[str, Any] = {}
    for name in strategies:
        strategy.update(STRATEGIES[name])
    strategy.update(custom_strategy)
    return strategy
