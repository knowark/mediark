import logging
from typing import Callable, Dict, Any
from .....application.domain.common import RecordList
from .....application.general.suppliers import EmailSupplier


class ConsoleEmailSupplier(EmailSupplier):
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()


    async def send(self, payload: Dict[str, Any]) -> dict:
        self.logger.info("Send email in console")
        self.logger.info("Content email")
        for item in payload:
            self.logger.info(item['context'])

        return payload

