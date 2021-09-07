from injectark import Injectark, Config
from schedulark import Task


class SendEmailJob:
    def __init__(self, injector: Injectark) -> None:
        self.config = injector.config
        self.injector = injector

    async def __call__(self, task: Task) -> dict:
        pass
