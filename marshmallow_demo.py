from marshmallow import Schema, fields, post_load


class Car:
    def __init__(self, name: str, brand: str):
        self.name = name
        self.brand = brand


class CarSchema(Schema):
    brand = fields.String(required=True)
    model = fields.String(required=True)

    @post_load
    def post_load(self, data):
        return Car(**data)
