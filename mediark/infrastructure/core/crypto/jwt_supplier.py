import json
import jwt
from typing import Dict


class JwtSupplier:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def encode(self, payload_dict: Dict, secret=None):
        secret = secret or self.secret
        return jwt.encode(payload_dict, secret,
                          algorithm='HS256').decode('utf-8')

    def decode(self, token: str, secret=None, verify=True):
        secret = secret or self.secret
        return jwt.decode(token, secret, verify=verify,
                          algorithms=['HS256'])
