import json
import jwt


class JwtSupplier:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def decode(self, token: str, secret=None, verify=True) -> dict:
        secret = secret or self.secret
        return jwt.decode(token, secret, verify=verify,
                          algorithms=['HS256'])
