from typing import Tuple, Dict, Any
from ....core import HttpClientSupplier


class SwiftAuthSupplier:
    def __init__(self,
                 client: HttpClientSupplier,
                 auth_url: str, username: str, password: str) -> None:
        self.client = client
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.expired_token = True

    async def authenticate(self) -> str:
        return 'my 123 token !!!'
