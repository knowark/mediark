class Image:
    def __init__(self, **attributes):
        self.namespace = attributes.get('namespace', '')
        self.reference = attributes.get('reference', '')
        self.extension = attributes.get('extension', 'jpg')
        self.url = attributes.get('url', '')
