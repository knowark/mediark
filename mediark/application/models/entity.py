from typing import TypeVar


class Entity:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')


T = TypeVar('T', bound=Entity)
