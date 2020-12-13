
from app.models.types import RelationshipType, StringType, BooleanType, IntegerType, FloatType, EmailType, DateTimeType, DateType, TimeType, TelephoneType, UrlType, PasswordType

type_mapper = {
    "relationship": RelationshipType,
    "boolean": BooleanType,
    "integer": IntegerType,
    "float": FloatType,
    "string": StringType,
    "email": EmailType,
    "datetime": DateTimeType,
    "date": DateType,
    "time": TimeType,
    "telephone": TelephoneType,
    "url": UrlType,
    "password": PasswordType
}
