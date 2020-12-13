
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

    def get_model_arguments(self):
        return {}

    def get_form_arguments(self):
        return {}
    
    def get_order_query_for_model(self):
        return f"{self.attribute.entity.get_name()}.{self.attribute.entity.get_main_attribute().name}"