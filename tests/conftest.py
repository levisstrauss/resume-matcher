import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.resume_matcher.main import app
from src.resume_matcher.core.database import Base, get_db
from src.resume_matcher.api.deps import get_db as api_get_db

# Use in-memory SQLite for tests
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[api_get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_job_data():
    """Sample job data for tests."""
    return {
        "title": "Senior Python Developer",
        "company": "Test Corp",
        "location": "Remote",
        "description": "Looking for a senior Python developer with experience in FastAPI and machine learning. Must have 5+ years of experience."
    }


@pytest.fixture
def sample_resume_text():
    """Sample resume text for tests."""
    return """
    John Doe
    Senior Software Engineer

    Experience:
    - 7 years of Python development
    - Expert in FastAPI and Django
    - Machine learning experience with PyTorch
    - Led team of 5 developers

    Education:
    - MS Computer Science, Stanford University

    Skills:
    Python, FastAPI, Django, PostgreSQL, Docker, Kubernetes, AWS
    """