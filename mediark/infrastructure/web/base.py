from flask import Flask
from flask_cors import CORS
from ..config import Config
from ..resolver import Registry
from .api import create_api


def create_app(config: Config, registry: Registry):
    app = Flask(__name__)
    CORS(app)
    app.config['SWAGGER'] = {
        'title': 'Mediark'
    }
    app.config['MEDIA'] = config['environment']['media']
    app.config.update(config['flask'])

    create_api(app, registry)

    return app
