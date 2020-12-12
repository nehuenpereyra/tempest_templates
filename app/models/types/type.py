
class Type:

    def __init__(self, attribute):
        self.attribute = attribute

    def is_relationship(self):
        return False

    def to_model(self):
        pass

    def to_form(self):
        pass

    def get_validations(self):
        return list()

    def get_widget(self):
        pass

    def get_form_arguments(self):
        return {}
