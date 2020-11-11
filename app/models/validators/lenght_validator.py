from .validator import Validator

class LenghtValidator(Validator):

    def __init__(self, min=-1, max=-1):
        self.min = min
        self.max = max

    def toForm(self):
        return f"Length(min={self.min}, max={self.max})"