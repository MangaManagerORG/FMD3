from sqlalchemy.orm import scoped_session, sessionmaker

from FMD3.Core.database import engine

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
