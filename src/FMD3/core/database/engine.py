from sqlalchemy import create_engine

from FMD3.constants import DB_PATH

engine = create_engine('sqlite:///'+DB_PATH.as_posix())
