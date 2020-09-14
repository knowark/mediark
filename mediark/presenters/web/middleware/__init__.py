from typing import List, Callable
from injectark import Injectark
from .authenticate import authenticate_middleware_factory


def middlewares(injector: Injectark) -> List[Callable]:
    return [
        authenticate_middleware_factory(injector)
    ]
