from fields.mutables import MutableBase
from fields.marshmallow_field import MarshmallowJSON
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


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
    __tablename__ = 'car'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String)
    engine = Column(Mutable.as_mutable(MarshmallowJSON(EngineSchema)))


def main():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/pycon_marshmallow', echo=False)
    session_maker = sessionmaker(bind=engine)
    session: Session = session_maker()

    car = Car('Ferrari')
    car.id = uuid4()
    car_id = car.id
    car.engine = MutableEngine('ENG1234', 'V12')

    session.add(car)
    session.commit()
    # expunge to prove query works
    session.expunge_all()
    car_copy = session.query(Car).get(car_id)
    print(f'Car {car_copy.name} has a {car_copy.engine.configuration} with serial number {car_copy.engine.serial_number}')
    car_copy.engine.configuration = 'V10'
    session.commit()
    car_copy2 = session.query(Car).get(car_id)
    print(f'Car {car_copy.name} has a {car_copy.engine.configuration} with serial number {car_copy.engine.serial_number}')


if __name__ == "__main__":
    main()
