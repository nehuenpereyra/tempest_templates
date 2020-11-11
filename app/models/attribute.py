
class Attribute:

    def __init__(self, name, label, default, searchable, entity):
        self.name = name
        self.label = label
        self.default = default
        self.searchable = searchable
        self.entity = entity
    
    def set_type(self, type):
        self.type = type  

    def set_validations(self, validations):
        self.validations = validations