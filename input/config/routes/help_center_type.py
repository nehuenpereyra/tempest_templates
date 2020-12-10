
import app.resources.api.help_center_type as api_help_center_type


def set_routes(app):

    app.add_url_rule("/api/tipos_centros",
                     "api_help_center_type_index", api_help_center_type.index)
