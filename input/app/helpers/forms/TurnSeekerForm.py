from .SpanishForm import SpanishForm
from wtforms import StringField, SubmitField, SelectField

from app.models.turn import Turn


class TurnSeekerForm(SpanishForm):
    search_query = StringField('Buscar')
    email = SelectField("Email", coerce=str)
    submit = SubmitField('Buscar')

    def __init__(self, *args, **kwargs):
        super(TurnSeekerForm, self).__init__(*args, **kwargs)
        emails = Turn.get_all_emails()
        emails.insert(0, "Elija alguno de los siguientes emails")
        self.email.choices = tuple(zip(emails, emails))
