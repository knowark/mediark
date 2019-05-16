from flask import Flask
from flask_cors import CORS
from ..config import Context
from .api import create_api
from .errors import register_error_handler


def create_app(context: Context):
    config = context.config
    registry = context.registry

    app = Flask(__name__)
    CORS(app)
    app.config.update(config['flask'])
    register_error_handler(app)
    create_api(app, registry)

    return app
