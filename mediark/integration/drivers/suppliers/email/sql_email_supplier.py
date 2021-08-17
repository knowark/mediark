from typing import Callable, Dict, Any
from aiosmtplib import send
from email.message import EmailMessage
from time import gmtime, strftime
from .....application.general.suppliers import EmailSupplier


class SqlEmailSupplier(EmailSupplier):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.sender = config['sender']
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.url = config['url']
        self.path = config['path']

    async def process(self, tenant: str, email: dict) -> None:
        template = email['template']
        context = email['context']
        #await super().notify(notification)

        #context = {'url': self.url, **notification}

        content = ""

        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = email['recipient']
        message['Subject'] = email['subject']
        message.add_header('Content-Type', 'text/html')
        message.set_payload(content)

        await send(message, hostname=self.host, port=self.port,
                   username=self.username, password=self.password,
                   use_tls=True)
