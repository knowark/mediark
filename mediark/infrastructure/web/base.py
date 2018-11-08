from flask import Flask
from flask_cors import CORS
# from ..config import Context
from .api import create_api


def create_app(context):
    registry = context.registry

    app = Flask(__name__)
    CORS(app)
    app.config['SWAGGER'] = {
        'title': 'Mediark'
    }

    create_api(app, registry)

    return app
