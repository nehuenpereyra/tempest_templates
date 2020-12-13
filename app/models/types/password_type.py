from .string_type import StringType

class PasswordType(StringType):

    def __init__(self, attribute, length):
        super().__init__(attribute, length, is_large=False)

    def __repr__(self):
        return f"Password({self.length})"

    def to_form(self):
        return "PasswordField"
    
    def to_from(self):
        return "wtforms"
    
    def to_import(self):
        return "PasswordField"
