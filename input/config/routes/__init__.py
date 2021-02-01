
from . import main
from . import auth
from . import setting
from . import handler


def set_routes(app):
    main.set_routes(app)
    auth.set_routes(app)
    setting.set_routes(app)
    handler.set_routes(app)
