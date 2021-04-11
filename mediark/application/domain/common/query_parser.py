from typing import List, Union, Callable, Sequence
from fnmatch import fnmatchcase
from .types import TermTuple


class QueryParser:
    def __init__(self) -> None:
        self.comparison_dict = {
            '=': lambda field, value: (
                lambda obj: getattr(obj, field) == value),
            '!=': lambda field, value: (
                lambda obj: getattr(obj, field) != value),
            '<=': lambda field, value: (
                lambda obj: getattr(obj, field) <= value),
            '<': lambda field, value: (
                lambda obj: getattr(obj, field) < value),
            '>': lambda field, value: (
                lambda obj: getattr(obj, field) > value),
            '>=': lambda field, value: (
                lambda obj: getattr(obj, field) >= value),
            'in': lambda field, value: (
                lambda obj: getattr(obj, field) in value),
            'like': lambda field, value: (
                lambda obj: self._parse_like(getattr(obj, field), value)),
            'ilike': lambda field, value: (
                lambda obj: self._parse_like(
                    getattr(obj, field), value, True)),
            'contains': lambda field, value: (
                lambda obj: value in getattr(obj, field)),
        }

        self.binary_dict = {
            '&': lambda expression_1, expression_2: (
                lambda obj: (expression_1(obj) and expression_2(obj))),
            '|': lambda expression_1, expression_2: (
                lambda obj: (expression_1(obj) or expression_2(obj)))
        }

        self.unary_dict = {
            '!': lambda expression_1: (
                lambda obj: (not expression_1(obj)))
        }

        self.default_join_operator = '&'

    def parse(self, domain: Sequence[Union[str, TermTuple]]) -> Callable:
        if not domain:
            return lambda obj: True
        stack = []  # type: List[Callable]
        for item in list(reversed(domain)):
            if isinstance(item, str) and item in self.binary_dict:
                first_operand = stack.pop()
                second_operand = stack.pop()
                function = self.binary_dict[str(item)](
                    first_operand, second_operand)
                stack.append(function)
            elif isinstance(item, str) and item in self.unary_dict:
                operand = stack.pop()
                stack.append(self.unary_dict[str(item)](operand))

            stack = self._default_join(stack)

            if isinstance(item, (list, tuple)):
                result = self._parse_term(item)
                stack.append(result)

        result = self._default_join(stack)[0]
        return result

    def _default_join(self, stack: List[Callable]) -> List[Callable]:
        operator = self.default_join_operator
        if len(stack) == 2:
            first_operand = stack.pop()
            second_operand = stack.pop()
            function = self.binary_dict[operator](
                first_operand, second_operand)
            stack.append(function)
        return stack

    def _parse_term(self, term_tuple: TermTuple) -> Callable:
        field, operator, value = term_tuple
        function = self.comparison_dict[operator]
        result = function(field, value)
        return result

    @staticmethod
    def _parse_like(value: str, pattern: str, insensitive=False) -> bool:
        if not isinstance(value, str):
            return False
        pattern = pattern.replace('%', '*').replace('_', '?')
        if insensitive:
            pattern = pattern.lower()
            value = value.lower()
        return fnmatchcase(value, pattern)
