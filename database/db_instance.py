from sqlalchemy import create_engine
from .config import db_string
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

db = create_engine(db_string)

Session = sessionmaker(bind=db)

Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class TelleModelMixin:

    def save_to_db(self, session):
        session.add(self)

    def destroy(self, session):
        session.delete(self)
