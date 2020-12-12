
import re

from app.models.types import IntegerType


class Entity:

    def __init__(self, name, label, order):
        self.name = name
        self.label = label
        self.order = order
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

    def get_main_attribute(self):
        return self.attributes.detect(lambda each: each.is_main, None)

    def add_attribute(self, attribute):
        self.attributes.add(attribute)
        attribute.entity = self

    def get_attribute(self, name):
        return self.attributes.detect(lambda each: each.name == name, None)

    def get_import_list_for_model(self):
        import_list = []
        relationship_attributes = self.attributes.select(
            lambda each: each.type.is_relationship() and each.type.has_cardinality_many_to_many()
        )

        if relationship_attributes:
            import_list.add("from .database_links import {}".format(
                ", ".join(relationship_attributes.collect(
                    lambda each: each.type.get_import_link()
                ))
            ))

        return import_list

    def has_relationship_attributes_for_form(self):
        return self.attributes.any_satisfy(
            lambda each: each.type.is_relationship() and each.is_loadable
        )

    def has_relationship_of_many_to_many(self):
        return self.attributes.any_satisfy(lambda each: each.type.is_relationship() and each.type.has_cardinality_many_to_many())

    def get_relationship_attributes_for_form(self):
        return self.attributes.select(
            lambda each: each.type.is_relationship() and each.is_loadable
        )

    def get_many_to_many_relationship_attributes(self):
        return self.attributes.select(lambda each: each.type.is_relationship() and each.type.has_cardinality_many_to_many())

    def get_model_import_for_form(self):

        import_list = []

        if self.attributes.any_satisfy(lambda each: each.validations[1].is_unique):
            import_list.add(self.get_name())

        import_list.extend(self.get_relationship_attributes_for_form().collect(
            lambda each: each.type.linked_attribute.entity.get_name()))

        import_list.remove_duplicated()

        if import_list:
            return "from app.models import {}".format(", ".join(import_list))
        return ""

    # def get_import_list_for_unique(self):
    #     if self.attributes.any_satisfy(lambda each: each.validations[1].is_unique):
    #         return f"from app.models import {self.name}"
    #     return ""

    def get_import_list_for_form(self):
        paths = {}
        paths[IntegerType(None).to_from()] = [IntegerType(None).to_form()]
        import_list = ""
        for attribute in self.attributes:
            if not attribute.type.to_from() in paths:
                paths[attribute.type.to_from()] = []
            if not paths[attribute.type.to_from()].includes(attribute.type.to_form()):
                paths[attribute.type.to_from()].add(attribute.type.to_form())

        for key, value in paths.items():
            import_list = import_list + "\n" + 'from {} import {}'.format(
                key,
                value.inject(lambda each, result: f"{result}, {each}", "")[2:]
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
                    if not paths[validation.to_from()].any_satisfy(lambda each: each == validation.to_import()):
                        paths[validation.to_from()].add(validation.to_import())

        for key, value in paths.items():
            import_list = import_list + "\n" + 'from {} import {}'.format(
                key,
                value.inject(lambda each, result: f"{result}, {each}", "")[2:]
            )
        return import_list

    def get_list_of_loadable_argument_names(self):
        return self.get_loadable_attributes().collect(lambda each: each.name)

    def get__list_args_resource(self):
        return ", ".join(self.get_loadable_attributes().collect(lambda each: f"{each.name} = form.{each.name}.data"))

    def get_loadable_attributes(self):
        return self.attributes.select(lambda each: each.is_loadable)
