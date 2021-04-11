import time
from modelark import Entity


class Media(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes.get('name', '')
        self.type = attributes.get('type', 'general')
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'jpg')
        self.uri = attributes.get('uri', '')
        self.timestamp = attributes.get('timestamp', int(time.time()))
