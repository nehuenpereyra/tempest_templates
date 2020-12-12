
from .type import Type


class DateTimeType(Type):

    def __repr__(self):
        return "DateTime"

    def to_model(self):
        return "DateTime"

    def to_form(self):
        return "DateTimeLocalField"
    
    def to_from(self):
        return "wtforms.fields.html5"
    
    def to_import(self):
        return "DateTimeLocalField"
    
    def get_form_arguments(self):
        return {
            "format": "'%Y-%m-%dT%H:%M'"
        }

    #def get_order_query_for_model(self):
    #    return f"({super().get_order_query_for_model()}, DateTime)"