from .validator import Validator


class EmailValidator(Validator):

    def __repr__(self):
        return "Email"

    def to_form(self):
        return "Email()"

    def to_from(self):
        return "wtforms.validators"
    
    def to_import(self):
        return "Email"
