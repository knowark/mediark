from typing import Any
from flask.views import MethodView
from injectark import Injectark


class DownloadResource:
    def __init__(self, injector: Injectark) -> None:
        self.directory_load_supplier = injector['DirectoryLoadSupplier']

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
