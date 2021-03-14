import phonenumbers
from wtforms.validators import ValidationError

def Telephone():
    def _valid_number(form, field):
        message = 'El numero ingresado no es válido.'
        try:
            if not (phonenumbers.is_valid_number(phonenumbers.parse(field.data, "AR"))):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _valid_number