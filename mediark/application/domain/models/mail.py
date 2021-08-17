from modelark import Entity


class Email(Entity):
    def __init__(self, **attributes)-> None:
        super(). __init__(**attributes)
        self.variables = attributes.get('variables', {})
        self.website_id = attributes['website_id']
        self.link = attributes.get('link', '')
        self.theme = attributes.get('theme', '')

