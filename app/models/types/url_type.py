
from .string_type import StringType


class UrlType(StringType):

    def __init__(self, attribute, length):
        super().__init__(attribute, length, is_large=False)
        self.length = length
        self.is_large = False

    def __repr__(self):
        return f"Url({self.length})"

    def to_form(self):
        return "URLField"

    def get_widget(self):
        return ""

    def to_from(self):
        return "wtforms.fields.html5"
    
    def to_import(self):
        return "URLField"