import re


class Entity:

    def __init__(self, name, order):
        self.name = name
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

    def has_relationship_of_many_to_many(self):
        return self.attributes.any_satisfy(lambda each: each.type.is_relationship() and each.type.has_cardinality_many_to_many())

    def get_many_to_many_relationship_attributes(self):
        return self.attributes.select(lambda each: each.type.is_relationship() and each.type.has_cardinality_many_to_many())

    # def __get_import_for(self, entity):
    #     return "link_{}_{}".format(
    #         self.get_name_delimited() if self.order < entity.order else entity.get_name_delimited(),
    #         entity.get_name_delimited() if self.order < entity.order else self.get_name_delimited()
    #     )
