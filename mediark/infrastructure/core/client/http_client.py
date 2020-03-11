from aiohttp import ClientSession


class HttpClientSupplier:
    def __init__(self):
        self.client = ClientSession()

    def __getattribute__(self, name):
        # Proxy all attribute/method accesses to self.client
        # Because inheriting from ClientSessions is discouraged in aiohttp
        return getattr(object.__getattribute__(self, 'client'), name)
