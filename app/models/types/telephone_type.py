
from .string_type import StringType
from app.models.validators import TelephoneValidator

class TelephoneType(StringType):

    def __init__(self, attribute, length):
        super().__init__(attribute, length, is_large=False)
        self.length = length
        self.is_large = False

    def __repr__(self):
        return f"Telephone({self.length})"

    def to_form(self):
        return "TelField"

    def get_widget(self):
        return ""
    
    def get_validations(self):
        return [TelephoneValidator(self.attribute)]

    def to_from(self):
        return "wtforms.fields.html5"
    
    def to_import(self):
        return "TelField"