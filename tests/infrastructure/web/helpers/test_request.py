import json
from flask import Flask, abort, request, jsonify
from mediark.infrastructure.web.helpers import get_request_filter


def test_request_filter():
    app = Flask(__name__)

    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 0

    @app.route("/test")
    def test():
        return jsonify(get_request_filter(request))

    response = app.test_client().get('/test?filter=[**BAD FILTER**]')
    data = json.loads(str(response.data, 'utf-8'))
    assert len(data[0]) == 0

    response = app.test_client().get('/test?limit=1&offset=2')
    data = json.loads(str(response.data, 'utf-8'))
    assert len(data[0]) == 0
    assert data[1] == 1
    assert data[2] == 2
