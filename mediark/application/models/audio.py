from .entity import Entity


class Audio(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'mp4')
        self.uri = attributes.get('uri', '')
