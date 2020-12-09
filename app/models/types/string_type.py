
from .type import Type


class StringType(Type):

    def __init__(self, attribute, length, is_large=False):
        super().__init__(attribute)
        self.length = length
        self.is_large = is_large

    def __repr__(self):
        return f"String({self.length})"

    def to_model(self):
        return f"String({str(self.length)})"

    def to_form(self):
        return "StringField"

    def get_widget(self):
        if self.is_large:
            return "TextArea()"
        return super().get_widget()

    def to_from(self):
        return "wtforms"
    
    def to_import(self):
        return "StringField"