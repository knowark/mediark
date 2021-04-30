import time
from modelark import Entity


class Media(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.type = attributes.get('type', 'general')
        self.size = attributes.get('size', 0)
        self.sequence = attributes.get('sequence', 0)
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'jpg')
        self.uri = attributes.get('uri', '')
        self.timestamp = attributes.get('timestamp', int(time.time()))
        self.path = attributes.get('path') or self.uri
