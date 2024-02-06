from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.orm import scoped_session

from . import engine
from .base import Base
from .engine import engine
from .models import *

# Create the tables
Base.metadata.create_all(engine)


# Create an instance of the scoped_session class
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
