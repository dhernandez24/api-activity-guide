import pytest

from api_activity.app import app, create_app


@pytest.fixture



def client():
    with create_app().test_client() as client:
        yield client

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200    
        
def test_profile_requires_auth(client):
    response = client.get('/profile', base_url="https://localhost")
    assert response.status_code == 401


def test_profile_with_valid_auth(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )
    response = client.get(
        '/profile',
        auth=("testuser", "testpass123"),
        base_url="https://localhost",
    )
    assert response.status_code == 200
    assert "testuser" in response.json["message"]


def test_own_endpoint_requires_auth(client):
    response = client.get('/own-endpoint', base_url="https://localhost")
    assert response.status_code == 401

def test_own_endpoint_with_valid_auth(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )
    response = client.get(
        '/own-endpoint',
        auth=("testuser", "testpass123"),
        base_url="https://localhost",
    )
    assert response.status_code == 200
    assert "testuser" in response.json["message"]







def test_square(client):
    response = client.get('/square/5')
    assert response.status_code == 200
    assert response.json == { "Shape": "Square", "Area": 25}

def test_echo(client):
    response = client.get('/echo?arg1=hello&arg2=world')
    assert response.status_code == 200
    assert response.json == {"arg1": "hello", "arg2": "world"}


