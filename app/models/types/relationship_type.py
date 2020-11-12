
from .type import Type


class RelationshipType(Type):

    def __init__(self, attribute, linked_entity, linked, cardinality):
        super().__init__(attribute)

        self.linked_attribute = None
        self.linked_attribute_presented = linked["attribute_presented"]
        self.cardinality = cardinality

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
