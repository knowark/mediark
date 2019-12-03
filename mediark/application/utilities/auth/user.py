
class User:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.name = attributes.get('name', '')
        self.email = attributes.get('email', '')
        self.roles = attributes.get('roles', [])
        self.attributes = attributes.get('attributes', {})
        self.authorization = attributes.get('authorization', {})
