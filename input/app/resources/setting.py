
from flask import redirect, render_template, request, url_for, abort, jsonify
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.alert import add_alert
from app.helpers.forms import SettingForm

from app.models import Setting, Alert


@permission('setting_update')
def edit():
    form = SettingForm(obj=Setting.get())
    return render_template("setting/update.html", form=form)


@permission('setting_update')
def update():
    form = SettingForm()
    if form.validate_on_submit():
        Setting.update(title=form.title.data, description=form.description.data, contact_email=form.contact_email.data,
                             items_per_page=form.items_per_page.data, enabled_site=form.enabled_site.data)
        add_alert(
            Alert("success", f"La configuración se actualizo correctamente."))
        return redirect(url_for("index"))
    return render_template("setting/update.html", form=form)
