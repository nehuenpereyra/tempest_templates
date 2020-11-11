
from .type import Type


class IntegerType(Type):

    def to_model(self):
        return "Integer"

    def to_form(self):
        return "IntegerField"
