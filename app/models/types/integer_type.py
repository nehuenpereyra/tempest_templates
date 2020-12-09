
from .type import Type


class IntegerType(Type):

    def __repr__(self):
        return "Integer"

    def to_model(self):
        return "Integer"

    def to_form(self):
        return "IntegerField"
    
    def to_from(self):
        return "wtforms"
    
    def to_import(self):
        return "IntegerField"

