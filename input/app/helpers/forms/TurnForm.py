from datetime import datetime
import phonenumbers

from .SpanishForm import SpanishForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.validators import ValidationError

from app.models.help_center import HelpCenter


def time_range(min, max):
    def _time_range(form, field):

        message = f'Debe ser un horario entre las {min} y antes de las {max} horas.'
        time = field.data.time()

        if (time.hour < min or time.hour >= max):
            raise ValidationError(message)

    return _time_range


def time_exact():
    def _time_exact(form, field):
        message = f'Debe ingresar una hora en punto o y media.'
        time = field.data.time()

        if (time.minute != 0 and time.minute != 30):
            raise ValidationError(message)

    return _time_exact


def unique():
    def _unique(form, field):
        message = f'Un turno en ese horario ya fue reservado.'
        if (HelpCenter.query.get(form.center_id.data).turns.any_satisfy(lambda each: each.day_hour == field.data)):
            raise ValidationError(message)
    return _unique


def time_invalid():
    def _time_invalid(form, field):
        message = f'Esa fecha no es valida.'

        if field.data <= datetime.today():
            raise ValidationError(message)

    return _time_invalid


def valid_number():
    def _valid_number(form, field):
        message = f'No es un numero valido.'
        try:
            if not (phonenumbers.is_valid_number(phonenumbers.parse(field.data, "AR"))):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _valid_number


class TurnForm(SpanishForm):

    id = IntegerField(widget=HiddenInput(), default=20)
    center_id = IntegerField(widget=HiddenInput(), default=0)
    email = EmailField('Correo Electrónico',
                       validators=[DataRequired(), Email()])
    donor_phone_number = StringField(
        'Telefono del donante', validators=[Optional(), Length(max=90), valid_number()])
    day_hour = DateTimeLocalField('Fecha y hora del turno',  format='%Y-%m-%dT%H:%M',
                                  validators=[DataRequired(), time_range(min=9, max=16), time_exact(), time_invalid(), unique()])

    submit = SubmitField('Guardar')
