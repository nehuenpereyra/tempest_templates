
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.fields.html5 import EmailField, TimeField, TelField, URLField
from wtforms.validators import ValidationError, Optional, DataRequired, Email, Length, URL

from app.models.help_center import HelpCenter
from app.models.help_center_type import HelpCenterType
from app.models.town import Town


def unique(class_, query_filter):
    """Returns true if there is no object with the same attribute in the database, otherwise it throws an exception.

    Keyword arguments:
    class_ -- class that will perform the query
    query_filter -- filter used to perform the query
    """

    def _unique(form, field):

        object_form = class_.query.get(form.id.data)
        object_db = class_.query.filter_by(
            **{query_filter: field.data}).first()

        if object_db and object_db != object_form:
            raise ValidationError(f'The value {field.data} is already loaded')

    return _unique


class HelpCenterApiForm(FlaskForm):

    id = IntegerField()
    nombre = StringField(validators=[DataRequired(), Length(max=16)])
    direccion = StringField(validators=[DataRequired(), Length(max=32)])
    telefono = TelField(
        validators=[DataRequired(), unique(HelpCenter, "phone_number")])
    hora_apertura = TimeField(validators=[DataRequired()])
    hora_cierre = TimeField(validators=[DataRequired()])

    tipo = SelectField(validators=[DataRequired()], coerce=str)
    municipio = SelectField(validators=[DataRequired()], coerce=str)

    web_url = URLField(validators=[Optional(), unique(HelpCenter, "web_url"), Length(
        max=64), URL()], filters=[lambda value: value if value else None])
    email = EmailField(validators=[Optional(), Email(), Length(max=32), unique(
        HelpCenter, "email")], filters=[lambda value: value if value else None])

    latitud = FloatField(validators=[Optional()])
    longitud = FloatField(validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(HelpCenterApiForm, self).__init__(*args, **kwargs)
        self.tipo.choices = HelpCenterType.query.all() \
            .collect(lambda each: (each.name, each.name))
        self.municipio.choices = Town.all().collect(lambda each: (each.name, each.name))
