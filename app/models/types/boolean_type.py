
from .type import Type


class BooleanType(Type):

    def __repr__(self):
        return "Boolean"

    def to_model(self):
        return "Boolean"

    def to_form(self):
        return "BooleanField"
