import pytest


@pytest.fixture
def client():
    """Create a test client to send requests to"""
    with app.test_client() as c:
        yield c
