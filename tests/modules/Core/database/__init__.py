# patch database with in-memory
from sqlalchemy import create_engine


from FMD3.core import database
database.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
