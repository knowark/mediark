from modelark import (
    Repository, RepositoryResolver, MemoryRepository)
from ...models import Media


class RepositoryService(RepositoryResolver):
    """Repository Resolver Service"""


class MediaRepository(Repository):
    model = Media


class MemoryMediaRepository(MemoryRepository, MediaRepository):
    """Memory Media Repository"""
