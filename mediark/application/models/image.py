from .entity import Entity


class Image(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'jpg')
        self.uri = attributes.get('uri', '')
