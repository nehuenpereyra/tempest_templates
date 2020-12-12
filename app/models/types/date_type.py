
from .type import Type


class DateType(Type):

    def __repr__(self):
        return "Date"

    def to_model(self):
        return "Date"

    def to_form(self):
        return "DateField"
    
    def to_from(self):
        return "wtforms.fields.html5"
    
    def to_import(self):
        return "DateField"