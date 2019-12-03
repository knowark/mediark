from typing import TypeVar


class Entity:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.created_at = attributes.get('created_at', 0)
        self.updated_at = attributes.get('updated_at', self.created_at)
        self.created_by = attributes.get('created_by', '')
        self.updated_by = attributes.get('updated_by', self.created_by)


T = TypeVar('T', bound=Entity)
