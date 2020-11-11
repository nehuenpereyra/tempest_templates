import re

class Entity:

    def __init__(self, name):
        self.name = name
        self.attributes = dict()
    
    def get_name(self):
        return self.name  
        
    def get_name_delimited(self):
        return re.sub("([A-Z])", "_\\1", self.name).strip().lower()[1:]

    def get_name_plural_delimited(self):
        name = self.get_name_delimited()
        if name[-1] == "y":
            return name[:-1] + "ies"
        return self.name + "s" 

    def add_attribute(self, attribute):
        self.attributes[attribute.name] = attribute
        attribute.entity = self

    def get_attribute(self, name):
        return self.attributes.get(name, None)