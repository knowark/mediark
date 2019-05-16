from traceback import format_tb
from werkzeug.exceptions import HTTPException

from flask import jsonify


def register_error_handler(app):

    def handle_error(error):
        code = 500
        if isinstance(error, HTTPException):
            code = error.code

        exception = type(error).__name__
        traceback = format_tb(error.__traceback__)

        return (
            jsonify(error=str(error), exception=exception, code=code,
                    traceback=traceback), code)

    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, handle_error)