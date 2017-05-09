from fields.mutables import MutableBase
from fields.marshmallow_field import MarshmallowJSON
from marshmallow import Schema, fields, post_load


class MutableEngine(MutableBase):
    def __init__(self, serial_number: str, configuration: str):
        self._serial_number = serial_number
        self._configuration = configuration

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @serial_number.setter
    def serial_number(self, name: str):
        self._serial_number = name
        self.changed()

    @property
    def configuration(self) -> str:
        return self._configuration

    @configuration.setter
    def configuration(self, brand: str):
        self._configuration = brand
        self.changed()


class EngineSchema(Schema):
    serial_number = fields.String()
    configuration = fields.String()

    @post_load
    def create_obj(self, data):
        return MutableEngine(data['serial_number'], data['configuration'])


Base = declarative_base()


class Car(Base):
    id = Column()
    engine = Column(Mutable.as_mutable(MarshmallowJSON(EngineSchema)))
