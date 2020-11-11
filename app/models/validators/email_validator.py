from .validator import Validator

class EmailValidator(Validator):

    def toForm(self):
        return "Email()"
