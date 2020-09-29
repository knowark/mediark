
from functools import partial
from injectark import Injectark
from ..helpers.schemas import MediaSchema
from ..helpers import missing
from .resource import Resource


class DownloadResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['FileInformer']

        super().__init__(
            MediaSchema,
            missing,
            partial(informer.load, 'media'),
            missing,
            missing)
