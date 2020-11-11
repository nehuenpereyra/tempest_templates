
from .type import Type


class FloatType(Type):

    def to_model(self):
        return "Float"

    def to_form(self):
        return "FloatField"
