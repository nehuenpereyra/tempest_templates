from .validator import Validator

class UniqueValidator(Validator):

    def __init__(self, is_unique):
        self.is_unique = is_unique

    def toForm(self):
        if self.is_unique
            return f"unique({self.atrribute.entity.get_name()}, {self.atrribute.name})"

    def toModel(self):
        if self.is_unique
            return "unique=True"
        return "unique=False"