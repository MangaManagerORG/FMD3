from sqlalchemy.orm import scoped_session, sessionmaker
from . import _engine
session_factory = sessionmaker(bind=_engine)
Session = scoped_session(session_factory)
