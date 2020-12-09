import re


class Entity:

    def __init__(self, name):
        self.name = name
        self.attributes = []

    def __repr__(self):
        return "[{}]\n{}".format(
            self.name,
            "\n".join(self.attributes.collect(lambda each: f"  {each}"))
        )

    def get_name(self):
        return self.name

    def get_name_delimited(self):
        return re.sub("([A-Z])", "_\\1", self.name).strip().lower()[1:]

    def get_name_plural_delimited(self):
        name = self.get_name_delimited()
        if name[-1] == "y":
            return name[:-1] + "ies"
        return name + "s"

    def add_attribute(self, attribute):
        self.attributes.add(attribute)
        attribute.entity = self

    def get_attribute(self, name):
        return self.attributes.detect(lambda each: each.name == name, None)

    def get_import_list_for_unique(self):
        if self.attributes.any_satisfy(lambda each: each.validations[1].is_unique == True):
            return f"from app.models import {self.name}"
        return ""
        
    def get_import_list_for_form(self):
        paths = {}
        import_list = ""
        for attribute in self.attributes:
            if not attribute.type.to_from() in paths:
                paths[attribute.type.to_from()] = []
            paths[attribute.type.to_from()].add(attribute.type.to_form())

        for key, value in paths.items(): 
            import_list = import_list +"\n"+ 'from {} import {}'.format(
                key,
                value.inject(lambda each, result: f"{result}, {each}", "")[1:]
            )
        return import_list

    def get_import_list_for_validations(self):
        paths = {}
        import_list = ""
        for attribute in self.attributes:
            for validation in attribute.validations:
                if validation.to_from():
                    if not validation.to_from() in paths:
                        paths[validation.to_from()] = []
                    if  not paths[validation.to_from()].any_satisfy(lambda each: each == validation.to_import()):
                        paths[validation.to_from()].add(validation.to_import())
                
        for key, value in paths.items():
            import_list = import_list +"\n"+ 'from {} import {}'.format(
                key,
                value.inject(lambda each, result: f"{result}, {each}", "")[1:]
            )
        return import_list