from .validator import Validator

class RequiredValidator(Validator):

    def __init__(self, is_required):
        self.is_required = is_required

    def toForm(self):
        if self.is_required
            return "DataRequired()"
        return "Optional()"

    def toModel(self):
        if self.is_required
            return "nullable=True"
        return "nullable=False"