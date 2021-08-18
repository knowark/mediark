from modelark import (
    Repository, RepositoryResolver, MemoryRepository)
from ...models import Media, Email


class RepositoryService(RepositoryResolver):
    """Repository Resolver Service"""


class MediaRepository(Repository):
    model = Media


class MemoryMediaRepository(MemoryRepository, MediaRepository):
    """Memory Media Repository"""


class EmailRepository(Repository):
    model = Email


class MemoryEmailRepository(MemoryRepository, EmailRepository):
    """Memory Email Repository"""
