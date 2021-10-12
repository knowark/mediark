import os
import ssl
import smtplib
from typing import Callable, Dict, Any
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .....application.domain.common import RecordList
from .....application.general.suppliers import EmailSupplier


class HttpEmailSupplier(EmailSupplier):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.sender = config['sender']
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.path = config['path']
        self.smtp = smtplib

    async def send(self, payload: RecordList) -> None:
        for record in payload:
            context = record['context']
            dir_name = os.path.dirname(record['template'])
            file_name = os.path.basename(record['template'])
            core_directory = Path(self.path)
            core_templates = str(core_directory / dir_name)

            complet_path = core_templates +"/" + file_name
            template_paths = [complet_path] + [core_templates]
            env = Environment(
            loader=FileSystemLoader(template_paths, followlinks=True),
            autoescape=select_autoescape(['html', 'xml']))
            html = env.get_template(file_name).render(**context)

            recipient = record['recipient']

            message = MIMEMultipart("alternative")
            message["Subject"] = record['subject']
            message["From"] = self.sender
            message["To"] = recipient
            part2 = MIMEText(html, "html")
            message.attach(part2)
            context = ssl.create_default_context()
            with self.smtp.SMTP_SSL(
                self.host, self.port, context=context) as server:
                print(f'Loging  with port {self.port}...')
                server.login(self.username, self.password)
                server.sendmail(self.sender, recipient, message.as_string())

