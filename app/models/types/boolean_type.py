
from .type import Type


class BooleanType(Type):

    def __repr__(self):
        return "Boolean"

    def to_model(self):
        return "Boolean"

    def to_form(self):
        return "BooleanField"
    
    def to_from(self):
        return "wtforms"
    
    def to_import(self):
        return "BooleanField"
