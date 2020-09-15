from aiohttp import ClientSession


class HttpClientSupplier:

    def __init__(self):
        self.client = None

    def __getattribute__(self, name):
        print("@"*120)
        print("antes de entrar al self client        ")
        print("self   client       ", self.client)
        print("@"*120)
        if self.client is None:
            print("@"*120)
            print("self client")
            print("@"*120)
            self.client = ClientSession()
            # Proxy all attribute/method accesses to self.client
            # Because inheriting from ClientSession is discouraged in aiohttp
            return getattr(object.__getattribute__(self, 'client'), name)
