from typing import List, Callable
from injectark import Injectark
from .authenticate import authenticate_middleware_factory
from .errors import errors_middleware_factory


def middlewares(injector: Injectark) -> List[Callable]:
    return [
        errors_middleware_factory(injector),
        authenticate_middleware_factory(injector)
    ]
