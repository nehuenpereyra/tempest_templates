import phonenumbers
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, SelectField, IntegerField, FloatField
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField, TimeField, TelField, URLField
from wtforms.validators import ValidationError, Optional, DataRequired, Email, Length

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


def valid_number():
    def _valid_number(form, field):
        message = f'No es un numero valido.'
        try:
            if not (phonenumbers.is_valid_number(phonenumbers.parse(field.data, "AR"))):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _valid_number


class HelpCenterForm(FlaskForm):

    id = IntegerField(widget=HiddenInput())
    name = StringField("Nombre", validators=[DataRequired(), Length(max=16)])
    address = StringField("Dirección", validators=[
                          DataRequired(), Length(max=32)])
    phone_number = TelField("Teléfono", validators=[
                            DataRequired(), unique(HelpCenter, "phone_number"), valid_number()])
    opening_time = TimeField("Hora de Apertura", validators=[DataRequired()])
    closing_time = TimeField("Hora de Cierre", validators=[DataRequired()])

    center_type = SelectField("Tipo de Centro", validators=[
                              DataRequired()], coerce=int)
    town = SelectField("Municipio", validators=[DataRequired()], coerce=int)

    web_url = URLField("Sitio Web", validators=[
                       Optional(), unique(HelpCenter, "web_url"), Length(max=64)], filters=[lambda value: value if value else None])
    email = EmailField("Correo Electrónico", validators=[
                       Optional(), Email(), Length(max=32), unique(HelpCenter, "email")], filters=[lambda value: value if value else None])
    view_protocol = FileField("Protocolo de Vista", validators=[
                              Optional(), FileAllowed(["pdf"], "El documento debe ser un pdf.")])
    latitude = FloatField("Latitud", validators=[
                          Optional()], widget=HiddenInput())
    longitude = FloatField("Longitud", validators=[
                           Optional()], widget=HiddenInput())

    published = BooleanField("Publicado", default=True)

    request_status = BooleanField("Aceptado")

    delete_view_protocol = BooleanField(
        "Eliminar Protocolo de Vista", default=False)

    submit = SubmitField("Enviar")

    def __init__(self, *args, **kwargs):
        super(HelpCenterForm, self).__init__(*args, **kwargs)
        self.center_type.choices = HelpCenterType.query.all() \
            .collect(lambda each: (each.id, each.name))
        self.town.choices = Town.all().collect(lambda each: (each.id, each.name))
