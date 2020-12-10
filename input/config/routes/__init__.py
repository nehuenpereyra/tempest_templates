from . import main
from . import user
from . import turn
from . import help_center
from . import help_center_type
from . import auth
from . import configuration
from . import handler


def set_routes(app):
    """Configure application paths

    Keyword arguments:
    app -- application to which the routes will be added
    """
    main.set_routes(app)
    user.set_routes(app)
    turn.set_routes(app)
    help_center.set_routes(app)
    help_center_type.set_routes(app)
    auth.set_routes(app)
    configuration.set_routes(app)
    handler.set_routes(app)
