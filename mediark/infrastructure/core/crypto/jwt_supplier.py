import json
import jwt


class JwtSupplier:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def encode(self, payload_dict: dict, secret: str = None) -> str:
        secret = secret or self.secret
        return jwt.encode(payload_dict, secret,
                          algorithm='HS256').decode('utf-8')

    def decode(
            self, token: str, secret: str = None, verify: bool = True) -> dict:
        secret = secret or self.secret
        return jwt.decode(token, secret, verify=verify,
                          algorithms=['HS256'])
