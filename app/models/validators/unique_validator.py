from .validator import Validator


class UniqueValidator(Validator):

    def __init__(self, attribute, is_unique):
        super().__init__(attribute)
        self.is_unique = is_unique

    def __repr__(self):
        if self.is_unique:
            return "Unique"
        return "No unique"
    
    def to_form(self):
        if self.is_unique:
            return f'Unique({self.attribute.entity.get_name()}, "{self.attribute.name}")'

    def to_model(self):
        if self.is_unique:
            return "unique=True"
        return "unique=False"
    
    def to_from(self):
        if self.is_unique:
            return "forms.utility"
    
    def to_import(self):
        if self.is_unique:
            return "Unique"
