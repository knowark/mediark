import time
from typing import Dict, Optional, Any
from .....core.http import HttpClientSupplier


class SwiftAuthSupplier:
    def __init__(self,
                 client: HttpClientSupplier,
                 auth_url: str, username: str, password: str) -> None:
        self.client = client
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.expires_at: Optional[time.struct_time] = None
        self.token: str = ""

    async def authenticate(self) -> str:
        if self.expires_at and time.gmtime() < self.expires_at:
            return self.token

        request = self._make_request()

        async with self.client.post(self.auth_url, json=request) as response:
            print("ENTRA AL SUPPLIER SWIFT>>>"*50)
            print(response.headers)
            self.token = response.headers['X-Subject-Token']
            payload = await response.json()
            self.expires_at = time.strptime(
                payload['token']['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

        return self.token

    def _make_request(self) -> Dict[str, Any]:
        return {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": self.username,
                            "domain": {
                                "name": "Default"
                            },
                            "password": self.password
                        }
                    }
                }
            }
        }
