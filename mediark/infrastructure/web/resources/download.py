from typing import Any
from aiohttp import web
from injectark import Injectark


class DownloadResource:
    def __init__(self, injector: Injectark) -> None:
        self.directory_load_supplier = injector['DirectoryLoadSupplier']

    async def get(self, request: web.Request) -> Any:
        """
        ---
        summary: Return all media.
        tags:
          - Download
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Download'
        """

        tenant = request.match_info.get('tenant')
        type = request.match_info.get('type')
        id_part_one = request.match_info.get('id_part_one')
        id_part_two = request.match_info.get('id_part_two')
        id = request.match_info.get('id')
        uri = f"{id_part_one}/{id_part_two}/{id}"

        path = self.directory_load_supplier.file_path(tenant, type, uri)
        return web.FileResponse(path)
