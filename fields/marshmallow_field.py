from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSON, JSONB
from uuid import UUID


class MarshmallowJSON(TypeDecorator):
    impl = JSON

    def __init__(self, schema, many: bool=None, strict: bool=True):
        super().__init__()
        self.schema = schema(strict=strict) if callable(schema) else schema
        self.strict = strict
        self.many = many

    def process_bind_param(self, value, dialect):
        if value is not None:
            value, errors = self.schema.dump(value, many=self.many)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value, errors = self.schema.load(value, many=self.many)
        return value

    def coerce_compared_value(self, op, value):
        self.impl.coerce_compared_value(op, value)


class MarshmallowJSONB(MarshmallowJSON):
    impl = JSONB


class UUIDListJSON(TypeDecorator):
    impl = JSON

    def __init__(self):
        super().__init__()

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = [str(uuid) for uuid in value]
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = [UUID(s) for s in value]
        return value
