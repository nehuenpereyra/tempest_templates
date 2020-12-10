from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class HelpCenterSeekerForm(FlaskForm):
    search_query = StringField('Buscar')
    help_center_state = RadioField(
        '', choices=[('pending', 'Pendientes'), ('rejected', 'Rechazados'), ('accepted', 'Aceptados')])
    submit = SubmitField('Buscar')
