
from app.models.types import RelationshipType


class Attribute:

    def __init__(self, name, label, default, searchable):
        self.name = name
        self.label = label
        self.default = default
        self.searchable = searchable
        self.type = None
        self.validations = None

    def get_type(self):
        return self.type

    def __repr__(self):
        validations_string = ", ".join(
            self.validations.collect(lambda each: str(each)))

        return f"{self.name}: {self.type} [{validations_string}]"

    def to_model(self):
        if self.type.__class__ != RelationshipType:
            return '__{} = db.Column("{}", db.{}{})'.format(
                self.name,
                self.name,
                self.type.to_model(),
                self.validations.select(lambda each: each.to_model())
                    .inject(lambda each, result: f"{result}, {each.to_model()}", "")
            )
        else:
            return '__{} = db.relationship("{}", back_populates="{}")'.format(
                self.name,
                self.type.linked_attribute.entity.get_name(),
                self.type.linked_attribute.name
            )

    def to_form(self):
        return '{} = {}("{}", validators=[{}])'.format(
                self.name,
                self.type.to_form(),
                self.label,
                self.validations.select(lambda each: each.to_form())
                    .inject(lambda each, result: f"{result}, {each.to_form()}", "")[1:]
            )