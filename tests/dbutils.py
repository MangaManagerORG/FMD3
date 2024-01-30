from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from FMD3.core.database.base import Base

def make_session():
    engine = create_engine('sqlite:///')

    # Define a many-to-many relationship between "Doors" and "Usuarios"
    # doors_usuarios = Table('doors_usuarios', Base.metadata,
    #     Column('door_id', Integer, ForeignKey('doors.id_puerta')),
    #     Column('usuario_rfid', String, ForeignKey('usuarios.rfid'))
    # )

    # Create the tables
    Base.metadata.create_all(engine)

    # Create an instance of the scoped_session class
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)