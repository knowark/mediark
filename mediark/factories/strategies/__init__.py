from injectark import StrategyBuilder
from .base import base
from .check import check
from .directory import directory
from .http import http
from .sql import sql
from .swift import swift


strategy_builder = StrategyBuilder({
    'base':  base,
    'check':  check,
    'directory':  directory,
    'http':  http,
    'sql': sql,
    'swift':  swift,
})
