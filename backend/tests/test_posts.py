import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.user import User
from app.models.post import Post
from app.core.security import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(test_db):
    db = TestingSessionLocal()
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_get_posts_short(test_db):
    response = client.get("/api/v1/posts/short")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_posts_long(test_db):
    response = client.get("/api/v1/posts/long")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_post(test_db, test_user):
    # First login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Create post
    post_data = {
        "title": "Test Post",
        "short_description": "Short test description",
        "long_description": "Long test description",
        "location": "Test Location, Bangalore",
        "latitude": 12.9716,
        "longitude": 77.5946
    }
    
    response = client.post(
        "/api/v1/posts/",
        json=post_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["username"] == "testuser" 