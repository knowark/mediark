import time
import unicodedata
from typing import Mapping
from ..exceptions import TenantLocationError, TenantCreationError


class Tenant:
    def __init__(self, **attributes):
        self.id = attributes['id']
        self.active = attributes.get('active', True)
        self.attributes = attributes.get('attributes', {})
        self.created_at = attributes.get('created_at', int(time.time()))
        self.data: Mapping[str, str] = attributes.get('data', {
            'memory': "",
            'directory':  "",
            'schema': ""
        })
        self.email = attributes.get('email', '')
        self.name = attributes['name']
        self.slug = self._normalize_slug(attributes.get('slug', self.name))
        self.updated_at = attributes.get('updated_at', self.created_at)
        self.zone = attributes.get('zone', '')

    def location(self, type: str = 'memory') -> str:
        if type not in self.data:
            raise TenantLocationError(
                f"No location found for '{type}' type "
                f"in tenant '{self.name}'.")
        return self.data[type]

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        stripped_slug = slug.strip().replace(" ", "_").lower()
        normalized_slug = unicodedata.normalize(
            'NFKD', stripped_slug).encode('ascii', 'ignore').decode('utf-8')
        if not normalized_slug:
            raise TenantCreationError("Invalid tenant 'slug' name.")
        return normalized_slug
