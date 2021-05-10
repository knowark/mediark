import time
from modelark import Entity


class Media(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.type = attributes.get('type', '')
        self.size = attributes.get('size', 0)
        self.sequence = attributes.get('sequence', 0)
        self.reference = attributes.get('reference', '')
        self.uri = attributes.get('uri', '')
        self.timestamp = attributes.get('timestamp', int(time.time()))
        self.path = attributes.get('path') or self.uri
