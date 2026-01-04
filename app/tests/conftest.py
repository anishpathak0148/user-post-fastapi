from httpx import ASGITransport, AsyncClient
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.auth import get_current_active_user
from app.database import Base
from app.dependencies import get_db
from app.helper.utils import get_hashed_password
from app.main import app
from app.schema.user import User as PydUser

TEST_DATABASE_URL = "sqlite:///:memory:"

# Use StaticPool so the in-memory SQLite database is shared across connections
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # Create tables
    # Use Base from app.database to create tables on the test engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    # create a test user in the DB and override dependencies
    unique = uuid.uuid4().hex
    test_user = models.User(
        name="test",
        email=f"test+{unique}@example.com",
        hashed_password=get_hashed_password("password"),
        is_active=True,
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    pyd_user = PydUser(
        id=test_user.id,
        name=test_user.name,
        email=test_user.email,
        is_active=test_user.is_active,
    )

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    def override_get_current_active_user():
        return pyd_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    client = TestClient(app)
    yield client

    # cleanup overrides
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_active_user, None)


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
