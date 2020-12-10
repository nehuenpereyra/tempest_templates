
from .type import Type


class RelationshipType(Type):

    def __init__(self, attribute, linked_entity, linked, cardinality, has_foreign_key=False):
        super().__init__(attribute)

        self.linked_attribute = None
        self.linked_attribute_presented = linked["attribute_presented"]
        self.cardinality = cardinality
        self.has_foreign_key = has_foreign_key
        self.mark = None

        if linked_entity:

            linked_attribute = linked_entity.get_attribute(linked["attribute"])

            if linked_attribute:
                self.linked_attribute = linked_attribute
                self.linked_attribute_presented = linked_entity \
                    .get_attribute(linked["attribute_presented"])

                inverse_relationship = self.linked_attribute.type

                inverse_relationship.linked_attribute = self.attribute
                inverse_relationship.linked_attribute_presented = self.attribute.entity \
                    .get_attribute(inverse_relationship.linked_attribute_presented)

                if self.__none_have_foreign_key() and self.__one_has_cardinality_one():
                    if inverse_relationship.has_cardinality_many():
                        self.has_foreign_key = True
                    else:
                        inverse_relationship.has_foreign_key = True

    def is_relationship(self):
        return True

    def __none_have_foreign_key(self):
        return not self.has_foreign_key and not self.linked_attribute.type.has_foreign_key

    def __one_has_cardinality_one(self):
        return self.has_cardinality_one() or self.linked_attribute.type.has_cardinality_one()

    def __repr__(self):
        if self.linked_attribute:
            linked_attribute_name = self.linked_attribute.name
        else:
            linked_attribute_name = "no linked"

        if type(self.linked_attribute_presented) is not str:
            linked_attribute_presented_name = self.linked_attribute_presented.name
        else:
            linked_attribute_presented_name = "no linked"

        return "Relationship({}, {})".format(
            linked_attribute_name,
            linked_attribute_presented_name
        )

    def has_cardinality_one(self):
        return self.cardinality == "one"

    def has_cardinality_many(self):
        return self.cardinality == "many"

    def has_cardinality_many_to_many(self):
        return self.has_cardinality_many() and \
            self.linked_attribute.type.has_cardinality_many()

    def get_import_link(self):
        own_entity = self.attribute.entity
        linked_entity = self.linked_attribute.entity

        return "link_{}_{}".format(
            own_entity.get_name_delimited() if own_entity.order < linked_entity.order
            else linked_entity.get_name_delimited(),

            linked_entity.get_name_delimited() if own_entity.order < linked_entity.order
            else own_entity.get_name_delimited()
        )

    def to_form(self):
        if self.cardinality == "one":
            return "SelectField"
        return "SelectMultipleField"

    def to_from(self):
        return "wtforms"

    def to_import(self):
        if self.cardinality == "one":
            return "SelectField"
        return "SelectMultipleField"
