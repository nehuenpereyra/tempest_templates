from . import main
# from . import configuration
# from . import handler


def set_routes(app):
    main.set_routes(app)
    # configuration.set_routes(app)
    # handler.set_routes(app)
