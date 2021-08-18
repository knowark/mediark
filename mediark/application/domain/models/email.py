import time
from modelark import Entity


class Email(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.template = attributes.get('template', '')
        self.context = attributes.get('context', {})
