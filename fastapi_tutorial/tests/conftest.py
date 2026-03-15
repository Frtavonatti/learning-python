"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models import user, post, comment  # Import models to register them


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "roles": ["user"]
    }


@pytest.fixture
def sample_user_data_2():
    """Another sample user data for testing."""
    return {
        "email": "test2@example.com",
        "username": "testuser2",
        "password": "testpass456",
        "roles": ["user"]
    }


@pytest.fixture
def create_test_user(client, sample_user_data):
    """Create a test user and return the response."""
    response = client.post("/auth/register", json=sample_user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_post_data(create_test_user):
    """Sample post data for testing."""
    return {
        "title": "Test Post",
        "content": "This is a test post content",
        "published": True,
        "rating": 5,
        "owner_id": create_test_user["id"]
    }


@pytest.fixture
def create_test_post(client, sample_post_data):
    """Create a test post and return the response."""
    response = client.post("/posts/", json=sample_post_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_comment_data(create_test_user, create_test_post):
    """Sample comment data for testing."""
    return {
        "text": "This is a test comment",
        "upvotes": 0,
        "downvotes": 0,
        "owner_id": create_test_user["id"],
        "post_id": create_test_post["id"]
    }
