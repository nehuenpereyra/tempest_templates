
from app.models.entity import Entity
from app.models.attribute import Attribute
from app.models.types.relationship_type import RelationshipType
from app.helpers.type_mapper import type_mapper
from app.helpers.validation_mapper import validation_mapper
from app.models.validators import RequiredValidator, UniqueValidator, LengthValidator


class EntityBuilder:

    def __init__(self):
        self.entities = dict()

    def add_entity(self, entity_json):
        entity = Entity(entity_json["name"])
        self.entities[entity.name] = entity

        for attribute_json in entity_json["attributes"]:
            attribute = Attribute(
                name=attribute_json["name"],
                label=attribute_json["label"],
                default=attribute_json.get("default", None),
                searchable=attribute_json.get("searchable", False)
            )
            entity.add_attribute(attribute)

            type_class = type_mapper[attribute_json["type"]["name"]]
            type_arguments = {**attribute_json["type"].get("arguments", dict()),
                              "attribute": attribute}

            if type_class is RelationshipType:
                entity_name = attribute_json["type"]["arguments"]["linked"]["class"]
                type_arguments["linked_entity"] = self.get_entity(entity_name)

            attribute.type = type_class(**type_arguments)

            validations = [
                RequiredValidator(attribute, False),
                UniqueValidator(attribute, False)
            ]
            validations.extend(attribute.type.get_validations())

            for validation_json in attribute_json.get("validations", list()):
                validation_part = validation_json.split("-")
                validation_class = validation_mapper[validation_part[0]]

                if validation_class is RequiredValidator:
                    validations[0].is_required = True
                elif validation_class is UniqueValidator:
                    validations[1].is_unique = True
                elif validation_class is LengthValidator:
                    validations.add(validation_class(attribute,
                                                     *validation_part[1:].collect(lambda each: int(each))))
                else:
                    validations.add(validation_class(attribute,
                                                     *validation_part[1:]))

            attribute.validations = validations

    def get_entity(self, entity_name):
        return self.entities.get(entity_name, None)

    def build(self):
        return list(self.entities.values())
