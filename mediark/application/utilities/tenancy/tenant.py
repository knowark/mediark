import time
import unicodedata


class Tenant:
    def __init__(self, **attributes):
        now = int(time.time())
        self.id = attributes.get('id', '')
        self.created_at = now
        self.updated_at = now
        self.name = attributes['name']
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
        self.slug = self._normalize_slug(attributes.get('slug', self.name))
        self.location = attributes.get('location', self.slug)

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        stripped_slug = slug.strip().replace(" ", "_").lower()
        normalized_slug = unicodedata.normalize(
            'NFKD', stripped_slug).encode('ascii', 'ignore').decode('utf-8')
        if not normalized_slug:
            raise ValueError("Invalid tenant 'slug' name.")
        return normalized_slug
