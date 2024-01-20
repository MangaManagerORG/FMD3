from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.db',isolation_level="SERIALIZABLE")
