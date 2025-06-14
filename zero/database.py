from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(bind=engine) as session:
        yield session
