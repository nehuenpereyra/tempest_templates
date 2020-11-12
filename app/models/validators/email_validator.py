from .validator import Validator


class EmailValidator(Validator):

    def __repr__(self):
        return "Email"

    def toForm(self):
        return "Email()"
