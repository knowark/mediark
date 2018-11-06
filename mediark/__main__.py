import os
from .infrastructure.config import Context
from .infrastructure.web import create_app, ServerApplication


def main():  # pragma: no cover
    context = Context()

    app = create_app(context)
    ServerApplication(app).run()


if __name__ == '__main__':  # pragma: no cover
    main()
