from .validator import Validator


class TelephoneValidator(Validator):

    def __repr__(self):
        return "Telephone"

    def to_form(self):
        return "Telephone()"

    def to_from(self):
        return "app.helpers.forms.validations.telephone"
    
    def to_import(self):
        return "Telephone"
