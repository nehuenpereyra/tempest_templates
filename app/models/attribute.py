from app.models.types import BooleanType

class Attribute:

    def __init__(self, name, label, default, searchable, is_main, is_loadable):
        self.name = name
        self.label = label
        self.default = default
        self.searchable = searchable
        self.is_main = is_main
        self.is_loadable = is_loadable
        self.type = None
        self.validations = None

    def get_type(self):
        return self.type

    def __repr__(self):
        validations_string = ", ".join(
            self.validations.collect(lambda each: str(each)))

        return f"{self.name}: {self.type} [{validations_string}]"

    def to_model(self):
        if not self.type.is_relationship():
            result = '{} = db.Column("{}", db.{}{})'.format(
                self.name,
                self.name,
                self.type.to_model(),
                self.validations.select(lambda each: each.to_model())
                    .inject(lambda each, result: f"{result}, {each.to_model()}", "")
            )
        else:
            linked_attribute = self.type.linked_attribute

            result = '{} = db.relationship("{}", back_populates="{}"{})'.format(
                self.name,
                linked_attribute.entity.get_name(),
                linked_attribute.name,
                f", secondary={self.type.get_import_link()}" if self.type.has_cardinality_many_to_many(
                ) else ""
            )

            if self.type.has_cardinality_one():
                if self.type.has_foreign_key:
                    result += '\n{}{} = db.Column("{}", db.Integer, db.ForeignKey("{}.id"){})'.format(
                        " " * 4,
                        f"{self.name}_id",
                        f"{self.name}_id",
                        linked_attribute.entity.get_name_delimited(),
                        self.validations.select(lambda each: each.to_model())
                            .inject(lambda each, result: f"{result}, {each.to_model()}", "")
                    )

        return result

    def to_form(self):
        return '{} = {}("{}", validators=[{}]{})'.format(
            self.name,
            self.type.to_form(),
            self.label,
            self.validations.select(lambda each: each.to_form())
            .inject(lambda each, result: f"{result}, {each.to_form()}", "")[1:],
            list(self.get_form_arguments().items()).inject(
                lambda each, result: "{}, {}={}".format(
                    result, each[0], each[1]
                ), ""
            )
        )

    def get_form_arguments(self):
        form_arguments = self.type.get_form_arguments()
        if self.default!=None or type(self.type)==BooleanType:
            form_arguments["default"] = ("False" if self.default==None else f"{self.default}")
        return form_arguments
