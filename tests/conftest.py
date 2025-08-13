import pytest
from app import create_app
from app.extensions import db
import os

@pytest.fixture
def client():
    # Use a separate test database
    os.environ["DATABASE_URI"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET_KEY"] = "test-secret"

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client
