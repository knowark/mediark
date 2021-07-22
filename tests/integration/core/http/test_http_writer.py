from os import name
from aiohttp import web
from pytest import fixture, raises
from mediark.integration.core.http import HttpResponseWriter


async def test_http_response_writer():

    config = {'uri': 'example/uri/file.png', 'type': 'image/png'}
    request = {'mock': 'request'}
    data = b'MOCK_BINARY_DATA'

    class MockStreamResponse(web.StreamResponse):
        request = None
        async def prepare(self, request):
            self.request = request

        async def write(self, data):
            self.data = data

    response = MockStreamResponse()
    response['request'] = request

    stream = HttpResponseWriter(response)

    await stream.setup(config)

    await stream.write(data)

    assert stream.response is response
    assert stream.response.content_type == 'image/png'
    assert stream.response.request == request
    assert stream.response.data == data
