
class Type:

    def __init__(self, builder, attribute):
        self.attribute = attribute

    def to_model(self):
        pass

    def to_form(self):
        pass

    def get_validators(self):
        return list()

    def get_widget(self):
        pass
