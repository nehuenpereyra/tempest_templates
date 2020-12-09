
from .type import Type


class FloatType(Type):

    def to_model(self):
        return "Float"

    def to_form(self):
        return "FloatField"
    
    def to_from(self):
        return "wtforms"
    
    def to_import(self):
        return "FloatField"
