from functools import partial
from injectark import Injectark
from ..helpers.schemas import MediaSchema
from ..helpers import missing
from .resource import Resource


class MediaResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['MediarkInformer']
        manager = injector['MediaStorageManager']

        super().__init__(
            MediaSchema,
            partial(informer.count, 'media'),
            partial(informer.search_media, 'media'),
            manager.store,
            missing)
