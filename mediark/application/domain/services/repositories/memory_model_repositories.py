from modelark import Repository, MemoryRepository


class MediaRepository(Repository):
    """Media Repository"""


class MemoryMediaRepository(MemoryRepository, MediaRepository):
    """Memory Media Repository"""
