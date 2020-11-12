
from .string_type import StringType
from app.models.validators import EmailValidator


class EmailType(StringType):

    def __init__(self, attribute, length):
        super().__init__(attribute, length, is_large=False)

    def __repr__(self):
        return f"Email({self.length})"

    def to_form(self):
        return "EmailField"

    def get_validations(self):
        return [EmailValidator(self.attribute)]
