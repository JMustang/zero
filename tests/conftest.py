import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from zero.app import app
from zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
def session():
    engine = create_engine(
        'sqlite:///:memory:', connect_args={'check_same_thread': False}
    )
    table_registry.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        yield session

    table_registry.metadata.drop_all(bind=engine)
