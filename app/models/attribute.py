
class Attribute:

    def __init__(self, name, label, default, searchable):
        self.name = name
        self.label = label
        self.default = default
        self.searchable = searchable
        self.type = None
        self.validations = None

    def __repr__(self):
        validations_string = ", ".join(
            self.validations.collect(lambda each: str(each)))

        return f"{self.name}: {self.type} [{validations_string}]"

    # def set_type(self, type):
    #     self.type = type

    # def set_validations(self, validations):
    #     self.validations = validations
