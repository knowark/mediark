from functools import partial
from injectark import Injectark
from ..helpers.schemas import MediaSchema
from ..helpers import missing
from .resource import Resource


class MediaResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        #informer = injector['MediarkInformer']
        informer = injector['HttpMediarkInformer']
        manager = injector['MediaStorageManager']

        super().__init__(
            MediaSchema,
            partial(informer.count, 'media'),
            partial(informer.search_media, 'media'),
            manager.store,
            missing)

    # def __init__(self, injector: Injectark) -> None:
    #     self.injector = injector
    #     self.media_storage_manager = self.injector[
    #         'MediaStorageManager']
    #     self.mediark_informer = self.injector['MediarkInformer']

    # async def head(self, request: web.Request) -> web.Response:
    #     """
    #     ---
    #     summary: Return medias HEAD headers.
    #     tags:
    #       - Media
    #     """

    #     domain, _, _ = get_request_filter(request)

    #     headers = {
    #         'Total-Count': str(len(
    #             await self.mediark_informer.search_media(domain)))
    #     }

    #     return web.Response(headers=headers)

    # async def get(self, request: web.Request) -> web.Response:
    #     """
    #     ---
    #     summary: Return all medias.
    #     tags:
    #       - Media
    #     responses:
    #       200:
    #         description: "Successful response"
    #         content:
    #           application/json:
    #             schema:
    #               type: array
    #               items:
    #                 $ref: '#/components/schemas/Media'
    #     """

    #     domain, limit, offset = get_request_filter(request)

    #     medias = MediaSchema().dump(
    #         await self.mediark_informer.search_media(domain), many=True)

    #     return web.json_response(medias, dumps=dumps)

    # async def put(self, request: web.Request) -> web.Response:
    #     """
    #     ---
    #     summary: Create or update an media.
    #     tags:
    #       - Media
    #     requestBody:
    #       required: true
    #       content:
    #         application/json:
    #           schema:
    #             $ref: '#/components/schemas/Media'
    #     responses:
    #       200:
    #         description: "Success"
    #     """
    #     media_records = MediaSchema(many=True).loads(await request.text())

    #     await self.media_storage_manager.store(media_records)

    #     return web.Response(status=200)
