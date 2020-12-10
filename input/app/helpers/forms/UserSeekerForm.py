from .SpanishForm import SpanishForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class UserSeekerForm(SpanishForm):
    search_query = StringField('Buscar')
    user_state = RadioField(
        '', choices=[('active', 'Activos'), ('blocked', 'Bloqueados')])
    submit = SubmitField('Buscar')
