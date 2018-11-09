class Audio:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'mp3')
        self.url = attributes.get('url', '')
