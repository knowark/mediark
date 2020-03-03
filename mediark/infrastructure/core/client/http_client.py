from aiohttp import ClientSession


class HttpClientSupplier(ClientSession):
    """Client Supplier to make HTTP requests."""
