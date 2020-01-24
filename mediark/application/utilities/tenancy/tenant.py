import time
import unicodedata
from typing import Mapping
from ..exceptions import TenantLocationError


class Tenant:
    def __init__(self, **attributes):
        now = int(time.time())
        self.id = attributes.get('id', '')
        self.name = attributes['name']
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
        self.slug = self._normalize_slug(attributes.get('slug', self.name))
        self.zone = attributes.get('zone', '')

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        stripped_slug = slug.strip().replace(" ", "_").lower()
        normalized_slug = unicodedata.normalize(
            'NFKD', stripped_slug).encode('ascii', 'ignore').decode('utf-8')
        if not normalized_slug:
            raise ValueError("Invalid tenant 'slug' name.")
        return normalized_slug
