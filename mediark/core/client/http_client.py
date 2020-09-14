from aiohttp import ClientSession


class HttpClientSupplier:

    def __init__(self):
        self.client = None

    def __getattribute__(self, name):
        if self.client is None:
            self.client = ClientSession()
        # Proxy all attribute/method accesses to self.client
        # Because inheriting from ClientSession is discouraged in aiohttp
        return getattr(object.__getattribute__(self, 'client'), name)
