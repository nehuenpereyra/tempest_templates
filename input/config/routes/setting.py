
from app.resources import setting


def set_routes(app):
    
    app.add_url_rule("/setting/edit",
                     "setting_edit", setting.edit)
    app.add_url_rule("/settings/update", "setting_update",
                     setting.update, methods=["POST"])
