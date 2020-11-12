
from app.models.validators import RequiredValidator, UniqueValidator, LengthValidator

validation_mapper = {
    "required": RequiredValidator,
    "unique": UniqueValidator,
    "length": LengthValidator
}
