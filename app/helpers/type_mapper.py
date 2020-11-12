
from app.models.types import RelationshipType, StringType, BooleanType, IntegerType, FloatType, EmailType

type_mapper = {
    "relationship": RelationshipType,
    "boolean": BooleanType,
    "integer": IntegerType,
    "float": FloatType,
    "string": StringType,
    "email": EmailType
}
