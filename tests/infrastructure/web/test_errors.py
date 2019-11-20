from flask import Flask, abort
from mediark.infrastructure.web.errors import register_error_handler


def test_handler_error():
    app = Flask(__name__)

    app.config['TESTING'] = True
    app.config['LIVESERVER_PORT'] = 0

    @app.route("/test")
    def test():
        abort(400, "Test error handled")

    register_error_handler(app)

    response = app.test_client().get("/test")

    assert response.status == '400 BAD REQUEST'
