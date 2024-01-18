from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, DateTime, Boolean, Float
from sqlalchemy.orm import sessionmaker, relationship
# Import the scoped_session class
from sqlalchemy.orm import scoped_session

from .base import Base
from .models import *

# Create the engine and the Session class

# engine = create_engine('sqlite:////home/pi/DATA/my_database.db')
_engine = create_engine('sqlite:///test.db',isolation_level="SERIALIZABLE")

# Define a many-to-many relationship between "Doors" and "Usuarios"
# doors_usuarios = Table('doors_usuarios', Base.metadata,
#     Column('door_id', Integer, ForeignKey('doors.id_puerta')),
#     Column('usuario_rfid', String, ForeignKey('usuarios.rfid'))
# )

# Create the tables
Base.metadata.create_all(_engine)


# Create an instance of the scoped_session class
from .Session import Session

session = Session
def get_session():
    return session
# def init_database():
