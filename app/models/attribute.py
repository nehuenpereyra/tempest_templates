from app.models.types import BooleanType


class Attribute:

    def __init__(self, name, label, default, is_searchable, is_main, is_loadable, show_in_detail):
        self.name = name
        self.label = label
        self.default = default
        self.is_searchable = is_searchable
        self.is_main = is_main
        self.is_loadable = is_loadable
        self.show_in_detail = show_in_detail
        self.type = None
        self.validations = None

    def get_type(self):
        return self.type

    def __repr__(self):
        validations_string = ", ".join(
            self.validations.collect(lambda each: str(each)))

        return f"{self.name}: {self.type} [{validations_string}]"

    def is_required(self):
        return self.validations[0].is_required

    def to_model(self):
        if not self.type.is_relationship():
            result = '__{} = db.Column("{}", db.{}{}{})'.format(
                self.name,
                self.name,
                self.type.to_model(),
                self.validations.select(lambda each: each.to_model())
                    .inject(lambda each, result: f"{result}, {each.to_model()}", ""),
                list(self.get_model_arguments().items()).as_string(
                    lambda each: ", {}={}".format(each[0], each[1])
                )
            )
        else:
            linked_attribute = self.type.linked_attribute

            result = '__{} = db.relationship("{}", back_populates="_{}__{}"{})'.format(
                self.name,
                linked_attribute.entity.get_name(),
                linked_attribute.entity.get_name(),
                linked_attribute.name,
                list(self.get_model_arguments().items()).inject(
                    lambda each, result: "{}, {}={}".format(
                        result, each[0], each[1]
                    ), ""
                )
            )

            if self.type.has_cardinality_one():
                if self.type.has_foreign_key:
                    result += '\n{}__{} = db.Column("{}", db.Integer, db.ForeignKey("{}.id"){})'.format(
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

    def get_model_arguments(self):
        return self.type.get_model_arguments()

    def get_form_arguments(self):

        arguments = self.type.get_form_arguments()

        if not self.is_required():
            arguments["filters"] = "[lambda value: value or {}]".format(
                "None" if not isinstance(self.type, BooleanType) else "False"
            )
        if self.entity.get_loadable_attributes().first() is self:
            arguments["render_kw"] = {"autofocus": True}
        if self.default != None or type(self.type) == BooleanType:
            arguments["default"] = (
                "False" if self.default == None else f"{self.default}")

        return arguments
