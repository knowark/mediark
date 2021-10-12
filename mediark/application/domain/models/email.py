import time
from modelark import Entity


class Email(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.recipient = attributes.get('recipient', '')
        self.subject = attributes.get('subject', '')
        self.type = attributes.get('type', '')
        self.template = attributes.get('template', '')
        self.context = attributes.get('context', {})
