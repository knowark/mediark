from flask import Flask
from flask_cors import CORS
from injectark import Injectark
from .api import create_api
from .errors import register_error_handler


def create_app(config, resolver: Injectark):
    app = Flask(__name__)
    CORS(app)
    app.config.update(config['flask'])

    register_error_handler(app)
    create_api(app, resolver)

    return app
