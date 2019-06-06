import json
import jwt
from typing import Any
from base64 import b64decode


class JwtSupplier:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def encode(self) -> Any:
        return

    def decode(self, token: str, secret=None, verify=True) -> Any:
        secret = secret or self.secret
        return jwt.decode(token, secret, verify=verify)
