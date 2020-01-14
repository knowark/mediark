from typing import Any
from flask.views import MethodView


class DownloadResource(MethodView):
    def __init__(self, resolver) -> None:
        self.directory_load_supplier = resolver['DirectoryLoadSupplier']

    def get(self, tenant: str, type: str, uri: str) -> Any:
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

        return self.directory_load_supplier.send_file(tenant, type, uri)
