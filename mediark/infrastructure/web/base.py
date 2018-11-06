from flask import Flask
from flask_cors import CORS
from ..config import Context


def create_app(context: Context):
    app = Flask(__name__)
    CORS(app)
    app.config['SWAGGER'] = {
        'title': 'Instark'
    }

    return app
