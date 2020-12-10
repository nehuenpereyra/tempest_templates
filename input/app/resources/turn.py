from datetime import date, timedelta, datetime
from flask import redirect, render_template, request, url_for, abort, Response, jsonify
from flask_login import login_user, login_required, current_user
from flask import abort

from app.models.turn import Turn
from app.models.alert import Alert
from app.models.configuration import Configuration
from app.models.help_center import HelpCenter
from app.helpers.forms.TurnForm import TurnForm
from app.helpers.permission import permission
from app.helpers.alert import add_alert, get_alert
from app.helpers.forms.TurnSeekerForm import TurnSeekerForm
import json


@login_required
@permission('turn_index')
def index():
    search_form = TurnSeekerForm(request.args)
    turns = Turn.get_next_tuns(search_query=search_form.search_query.data,
                               email=search_form.email.data,
                               page=int(request.args.get('page', 1)),
                               per_page=Configuration.query.first().pagination_elements)

    return render_template("turn/index.html", turns=turns, alert=get_alert(), search_form=search_form)


@login_required
@permission('turn_index')
def center_index(id):
    search_form = TurnSeekerForm(request.args)
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("help_center_index"))

    if center.is_in_pending_state():
        add_alert(Alert(
            "danger", "No se puede acceder ya que el centro esta pendiente de aceptación."))
        return redirect(url_for("help_center_index"))

    if center.is_in_rejected_state():
        add_alert(
            Alert("danger", "No se puede acceder ya que el centro esta rechazado."))
        return redirect(url_for("help_center_index"))

    turns = Turn.search(id_center=id, email=search_form.email.data, page=int(request.args.get('page', 1)),
                        per_page=Configuration.query.first().pagination_elements)

    return render_template("turn/center_index.html", id_center=id, turns=turns, alert=get_alert(), name_center=center.name, search_form=search_form)


@login_required
@permission('turn_create')
def new(id):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))
    return render_template("turn/new.html", center_id=id, form=TurnForm(), name_center= center.name)


@login_required
@permission('turn_create')
def create(id):

    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    form = TurnForm(center_id=id, id=None)

    if form.validate_on_submit():
        turn = Turn(help_center=center,
                    email=form.email.data,
                    donor_phone_number=form.donor_phone_number.data,
                    day_hour=form.day_hour.data)
        turn.save()
        add_alert(
            Alert("success", f"El turno con fecha {turn.day_hour.strftime('%Y/%m/%d-%H:%M:%S')} de {turn.email} se creo correctamente."))
        return redirect(url_for("turn_center_index", id=id))

    return render_template("turn/new.html", center_id=id, form=form, name_center= center.name)


@login_required
@permission('turn_update')
def edit(id, id_turn):
    turn = Turn.query.get(id_turn)
    center = HelpCenter.query.get(id)

    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("help_center_index"))

    if not turn:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    if not center.turns.any_satisfy(lambda each: each.id == turn.id):
        add_alert(Alert("danger", "El centro no tiene ese turno asignado."))
        return redirect(url_for("turn_center_index", id=id))

    return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=TurnForm(obj=turn), name_center=center.name)


@login_required
@permission('turn_update')
def update(id, id_turn):
    form = TurnForm(center_id=id)
    print(form.center_id.data)

    if not form.validate_on_submit():
        return render_template("turn/edit.html", id_center=id, id_turn=id_turn, form=form, name_center= HelpCenter.query.get(id).name)

    turn = Turn.update(id_turn, id, form.email.data,
                       form.donor_phone_number.data, form.day_hour.data)

    if not form:
        add_alert(Alert("danger", "El turno no existe."))
        return redirect(url_for("turn_center_index", id=id))

    add_alert(
        Alert("success", f"El turno de {turn.email} se actualizo correctamente."))

    return redirect(url_for("turn_center_index", id=id))


@login_required
@permission('turn_delete')
def delete(id, id_turn):
    center = HelpCenter.query.get(id)
    if not center:
        add_alert(Alert("danger", "El centro no existe."))
        return redirect(url_for("turn_center_index", id=id))

    if center.has_turn(Turn.query.get(id_turn)):
        turn = Turn.delete(id_turn)
        add_alert(
            Alert("success", f"El turno de {turn.email} se borro con exito."))
    else:
        add_alert(Alert("danger", "El turno no existe."))

    return redirect(url_for("turn_center_index", id=id))

def quantity_turns_last():
    return jsonify(Turn.get_quantity_turns_last())


def free_time(id):

    # Se comprueba que el centro exista
    center = HelpCenter.query.get(id)
    if not center:
        abort(404)

    # Si el centro no esta aceptado retorna error 400
    if not center.is_in_accepted_state():
        abort(404)

    # Se establece la fecha actual para buscar turnos libres
    search_date = date.today()

    # Si se envia una fecha por parametro se la establece para buscar turnos libres
    if request.args.get('fecha'):
        try:
            search_date = datetime.strptime(
                request.args.get('fecha'), '%d-%m-%Y').date()
        except ValueError:
            abort(500)

    send_data = json.loads(Turn.all_free_time_json(id, search_date))
    send_data["centro"] = HelpCenter.get(id).name

    return Response(response=json.dumps(send_data), status=200, mimetype="application/json")


def reserved(id):

    data = request.json
    print(request.json)

    try:
        # Se comprueba que el centro exista
        center = HelpCenter.query.get(data["centro_id"])
        if not center or (data["centro_id"] != id):
            abort(400)

        # Si el centro no esta aceptado retorna error 400
        if not center.is_in_accepted_state():
            abort(400)

        # Se realiza la conversion de string a datetime
        data_time_init = datetime.strptime(
            f"{data['fecha']} - {data['hora_inicio']}:00", '%Y-%m-%d - %H:%M:%S')
        data_time_end = datetime.strptime(
            f"{data['fecha']} - {data['hora_fin']}:00", '%Y-%m-%d - %H:%M:%S')

        # Se comprueba que la diferencia sea de media hora
        if ((data_time_end-data_time_init).total_seconds() / 60) != 30:
            abort(400)

        # Se establece el campo de telefono de donante en una cadena vacia por si no envio ese campo
        donor_phone_number = ""
        if 'telefono_donante' in data:
            donor_phone_number = data['telefono_donante']

        # Se crea uns instancia del formulario con los datos recibidos
        form = TurnForm(id=None, day_hour=data_time_init,
                        center_id=id, email=data['email_donante'],
                        donor_phone_number=donor_phone_number, meta={'csrf': False})

        # Se validan los datos recibidos
        if form.validate_on_submit():
            Turn(help_center=center,
                 email=form.email.data,
                 donor_phone_number=form.donor_phone_number.data,
                 day_hour=form.day_hour.data).save()

            # Respuesta que se le entrega al cliente
            # Si envia campos demas no seran utilizados en la respuesta
            response = {
                "atributos":
                {
                    "centro_id": data["centro_id"],
                    "email_donante": data["email_donante"],
                    "hora_inicio": data["hora_inicio"],
                    "hora_fin": data["hora_fin"],
                    "fecha": data["fecha"]
                }
            }
            if 'telefono_donante' in data:
                response["atributos"]["telefono_donante"] = data["telefono_donante"]

            return jsonify(response)
        else:
            # Si no cumple con alguna de las validaciones
            print("El fomulario es Incorrecto o ya esta cargado")
            abort(400)

    except Exception as e:
        # Si existe alguna excepción imprime la excepción
        print(f"Excepción: {e}")
        abort(400)
