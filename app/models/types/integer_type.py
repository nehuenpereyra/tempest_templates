
from .type import Type


class IntegerType(Type):

    def __repr__(self):
        return "Integer"

    def to_model(self):
        return "Integer"

    def to_form(self):
        return "IntegerField"
