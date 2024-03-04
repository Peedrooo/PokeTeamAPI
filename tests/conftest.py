from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import sys
import pytest
import models

from database import get_db
from main import app


try:
    sys.path.append(os.getcwd() + "/src")
except Exception:
    pass


engine = create_engine(
    "sqlite:///test.db",
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def session():
    session = TestingSessionLocal()
    yield session
    os.remove("test.db")


@pytest.fixture(scope="function")
def client(session) -> TestClient:
    def get_db_test():
        db = session
        try:
            yield db
        finally:
            db.close()

    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_db_test
        yield client
