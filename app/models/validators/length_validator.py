from .validator import Validator


class LengthValidator(Validator):

    def __init__(self, attribute, min=-1, max=-1):
        super().__init__(attribute)
        self.min = min
        self.max = max

    def __repr__(self):
        return f"Length({self.min}, {self.max})"

    def toForm(self):
        return f"Length(min={self.min}, max={self.max})"
