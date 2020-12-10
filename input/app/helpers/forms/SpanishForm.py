from flask_wtf import FlaskForm


class SpanishForm(FlaskForm):
    class Meta:
        locales = ['es_ES', 'es']
