
from flask import url_for, redirect, render_template, request
from flask_login import login_required

from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert
from app.helpers.forms.HelpCenterSeekerForm import HelpCenterSeekerForm

from app.helpers.forms.HelpCenterForm import HelpCenterForm
from app.models.alert import Alert
from app.models.configuration import Configuration
from app.models.help_center import HelpCenter
from app.models.help_center_type import HelpCenterType
from app.models.town import Town


@login_required
@permission('help_center_index')
def index():
    search_form = HelpCenterSeekerForm(request.args)

    help_centers = HelpCenter.search(search_query=search_form.search_query.data,
                                     help_center_state=search_form.help_center_state.data,
                                     page=int(request.args.get('page', 1)),
                                     per_page=Configuration.query.first().pagination_elements)

    return render_template("help_center/index.html", help_centers=help_centers, search_form=search_form, alert=get_alert())


@login_required
@permission('help_center_create')
def new():
    return render_template("help_center/new.html", form=HelpCenterForm())


@ login_required
@ permission('help_center_create')
def create():
    form = HelpCenterForm(id=None)

    if not form.validate_on_submit():
        return render_template("help_center/new.html", form=form)

    center_type = HelpCenterType.get(form.center_type.data)
    town = Town.get(form.town.data)

    help_center = HelpCenter(name=form.name.data, address=form.address.data, phone_number=form.phone_number.data,
                             opening_time=form.opening_time.data, closing_time=form.closing_time.data,
                             center_type=center_type, town=town, web_url=form.web_url.data, email=form.email.data,
                             view_protocol=form.view_protocol.data, latitude=form.latitude.data,
                             longitude=form.longitude.data, published=form.published.data, request_status=True)
    help_center.save()
    add_alert(Alert(
        "success", f"El centro de ayuda \"{help_center.name}\" fue cargado con exito."))

    return redirect(url_for("help_center_index"))


@login_required
@permission('help_center_update')
def edit(id):

    help_center = HelpCenter.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe."))
        return redirect(url_for("help_center_index"))

    form = HelpCenterForm(obj=help_center)
    form.center_type.data = help_center.center_type.id
    form.town.data = help_center.town.id

    return render_template("help_center/edit.html", form=form, help_center=help_center)


@login_required
@permission('help_center_update')
def update(id):

    help_center = HelpCenter.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe."))
        return redirect(url_for("help_center_index"))

    form = HelpCenterForm(id=id)

    if not form.validate_on_submit():
        return render_template("help_center/edit.html", form=form, help_center=help_center)

    help_center.name = form.name.data
    help_center.address = form.address.data
    help_center.phone_number = form.phone_number.data
    help_center.opening_time = form.opening_time.data
    help_center.closing_time = form.closing_time.data
    help_center.center_type = HelpCenterType.get(form.center_type.data)
    help_center.town = Town.get(form.town.data)
    help_center.web_url = form.web_url.data
    help_center.email = form.email.data
    help_center.published = form.published.data
    help_center.latitude = form.latitude.data
    help_center.longitude = form.longitude.data

    if form.delete_view_protocol.data and help_center.has_view_protocol:
        help_center.view_protocol = None
    elif form.view_protocol.data:
        help_center.view_protocol = form.view_protocol.data

    if not help_center.is_in_pending_state():
        help_center.request_status = form.request_status.data

    help_center.save()

    add_alert(Alert(
        "success", f"El centro de ayuda {help_center.name} se actualizo correctamente."))

    return redirect(url_for("help_center_index"))


@ login_required
@ permission('help_center_show')
def show(id):
    help_center = HelpCenter.query.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe."))
        return redirect(url_for("help_center_index"))

    return render_template("help_center/show.html", help_center=help_center, alert=get_alert(),
                           view_protocol_filename=f"uploads/protocolos/{ help_center.get_view_protocol_filename() }")


@ login_required
@ permission('help_center_delete')
def delete(id):
    center = HelpCenter.query.get(id)

    if center:
        center.remove()
        alert = Alert(
            "success", f'El centro de ayuda "{center.name}" fue eliminado con exito.')
    else:
        alert = Alert("danger", "El centro de ayuda no existe.")

    add_alert(alert)
    return redirect(url_for("help_center_index"))


@ login_required
@ permission('help_center_certify')
def certify(id, is_accepted):
    help_center = HelpCenter.query.get(id)

    if not help_center:
        add_alert(Alert("danger", "El centro de ayuda no existe"))
        return redirect(url_for("help_center_index"))

    center_state_message = {
        False: "rechazado",
        True: "aceptado"
    }

    if not help_center.is_in_pending_state():
        add_alert(Alert(
            "danger", f"El centro de ayuda se encuentra actualmente {center_state_message[help_center.is_in_accepted_state()]}"))
        return redirect(url_for("help_center_show", id=id))

    if is_accepted:
        help_center.accept_request()
    else:
        help_center.reject_request()

    help_center.save()

    add_alert(Alert(
        "success", f"El centro de ayuda fue {center_state_message[is_accepted]} con exito"))
    return redirect(url_for("help_center_show", id=id))
