from fields.marshmallow_field import MarshmallowJSON
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Engine:
    def __init__(self, serial_number: str, configuration: str):
        self.serial_number = serial_number
        self.configuration = configuration


class EngineSchema(Schema):
    serial_number = fields.String()
    configuration = fields.String()

    @post_load
    def create_obj(self, data):
        return Engine(data['serial_number'], data['configuration'])


Base = declarative_base()


class Car(Base):
    __tablename__ = 'car'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String)
    engine = Column(MarshmallowJSON(EngineSchema))


def main():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/pycon_marshmallow', echo=True)  # Turn on echo to follow sqlalchemy session
    session_maker = sessionmaker(bind=engine)
    session: Session = session_maker()

    car = Car(name='Ferrari')
    car.id = uuid4()
    car_id = car.id
    car.engine = Engine('ENG1234', 'V12')

    session.add(car)
    session.commit()
    # expunge to prove query works
    session.expunge_all()
    car_copy = session.query(Car).get(car_id)
    # prints Car Ferrari has a V12 with serial number ENG1234
    print(f'Car {car_copy.name} has a {car_copy.engine.configuration} with serial number {car_copy.engine.serial_number}')


if __name__ == "__main__":
    main()
