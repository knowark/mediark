from traceback import format_tb
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify

from flask import jsonify


def register_error_handler(app: Flask):

    def handle_error(error):
        code = error.code or 500

        exception = type(error).__name__
        traceback = format_tb(error.__traceback__)
        return jsonify(error={
            'exception': exception,
            'message': str(error),
            'trace': traceback
        }), code

    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, handle_error)
