
from .type import Type


class TimeType(Type):

    def __repr__(self):
        return "Time"

    def to_model(self):
        return "Time"

    def to_form(self):
        return "TimeField"
    
    def to_from(self):
        return "wtforms.fields.html5"
    
    def to_import(self):
        return "TimeField"