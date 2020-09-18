from aiohttp import ClientSession


class HttpClientSupplier:

    def __init__(self):
        self.client = None

    def __getattr__(self, name):

        if self.client is None:
            self.client = ClientSession()

        # Proxy all attribute/method accesses to self.client
        # Because inheriting from ClientSession is discouraged in aiohttp
        # return getattr(object.__getattr__(self, 'client'), name)
        return getattr(self.client, name)
