from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database initialized and an engine object is created.
DBURL = "sqlite:///inspections.db"
engine = create_engine(DBURL)


# Here, a class required for all database models is declared.
class Base(DeclarativeBase):
    pass

# Here, we initialize a sessionmaker object
SessionLocal = sessionmaker(bind=engine)