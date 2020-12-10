
from app.resources import help_center
import app.resources.api.help_center as api_help_center


def set_routes(app):

    app.add_url_rule("/centros", "help_center_index", help_center.index)
    app.add_url_rule("/centro/ver/<int:id>",
                     "help_center_show", help_center.show)
    app.add_url_rule("/centro/nuevo", "help_center_new", help_center.new)
    app.add_url_rule("/centro/crear", "help_center_create",
                     help_center.create, methods=["POST"])
    app.add_url_rule("/centro/editar/<int:id>",
                     "help_center_edit", help_center.edit)
    app.add_url_rule("/centro/actualizar/<int:id>",
                     "help_center_update", help_center.update, methods=["POST"])
    app.add_url_rule("/centro/borrar/<int:id>",
                     "help_center_delete", help_center.delete)
    app.add_url_rule("/centro/aceptar/<int:id>",
                     "help_center_accept", help_center.certify, defaults={"is_accepted": True})
    app.add_url_rule("/centro/rechazar/<int:id>",
                     "help_center_reject", help_center.certify, defaults={"is_accepted": False})

    app.add_url_rule("/api/centros", "api_help_center_index",
                     api_help_center.index)
    app.add_url_rule("/api/centro/<int:id>",
                     "api_help_center_show", api_help_center.show)
    app.add_url_rule("/api/centro", "api_help_center_create",
                     api_help_center.create, methods=["POST"])
    app.add_url_rule("/api/centros/mas_turnos", "api_help_center_more_turns",
                     api_help_center.more_turns)
