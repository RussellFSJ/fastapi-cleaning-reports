from bson.objectid import ObjectId


# overwriting ObjectId to be validated by Pydantic models
# https://stackoverflow.com/a/59503870
class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError("ObjectId required")
        return str(v)
