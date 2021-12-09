from aiohttp import ClientSession, ClientTimeout


class HttpClientSupplier:

    def __init__(self):
        self.client = None

    def __getattr__(self, name):

        if self.client is None:
            session_timeout = ClientTimeout(
                total=None,sock_connect=None,sock_read=None)

            self.client = ClientSession(timeout=session_timeout)

        # Proxy all attribute/method accesses to self.client
        # Because inheriting from ClientSession is discouraged in aiohttp
        # return getattr(object.__getattr__(self, 'client'), name)
        return getattr(self.client, name)

    def __del__(self):
        self.client and asyncio.run(self.client.close())

