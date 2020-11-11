
from .type import Type


class StringType(Type):

    def __init__(self, builder, attribute, length, is_large):
        super().__init__(builder, attribute)
        self.length = length
        self.is_large = is_large

    def to_model(self):
        return f"String({str(self.length)})"

    def to_form(self):
        return "StringField"

    def get_widget(self):
        if self.is_large:
            return "TextArea()"
        return super().get_widget()
