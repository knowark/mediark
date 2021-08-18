import smtplib
import ssl
from typing import Callable, Dict, Any
from aiosmtplib import send
from email.message import EmailMessage
from time import gmtime, strftime
from .....application.general.suppliers import EmailSupplier


class HttpEmailSupplier(EmailSupplier):
    def __init__(self, config: Dict[str, Any]) -> None:
        print(config)
        self.sender = config['sender']
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']

    async def send(self, payload: dict) -> None:
        recipient = payload['recipient']
        message = str(payload['context'])
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            print(f'Loging into gmail with port {self.port}...')
            server.login(self.sender, self.password)

            server.sendmail(self.sender, recipient, message)

