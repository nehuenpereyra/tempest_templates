from .validator import Validator


class RequiredValidator(Validator):

    def __init__(self, attribute, is_required):
        super().__init__(attribute)
        self.is_required = is_required

    def __repr__(self):
        if self.is_required:
            return "Required"
        return "Optional"

    def toForm(self):
        if self.is_required:
            return "DataRequired()"
        return "Optional()"

    def toModel(self):
        return f"nullable={not self.is_required}"
