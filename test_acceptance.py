from flask import session
from app import app
import uuid
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login(client):
    response = client.post('/login', data={
        'username': 'admin_login',
        'password': 'password'
    })

    # Check that the response redirects to /dashboard
    assert response.status_code == 302
    assert response.headers['Location'] == '/dashboard'

    # Check that the session contains the correct username
    with client.session_transaction() as session:
        assert session['username'] == 'admin_login'

    # Test with invalid credentials
    response = client.post('/login', data={
        'username': 'invalid_username',
        'password': 'invalid_password'
    })

    # Check that the response contains an error message
    assert b'Invalid credentials' in response.data

# test for registration with invalid email address
def test_register_invalid_email(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'example.com',
        'username': "testuser",
        'password': 'password',
        'confirm_password': 'password'
    })

    assert b'Invalid email address' in response.data

# test for registration with invalid username
def test_register_invalid_username(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'username': "test",
        'password': 'password',
        'confirm_password': 'password'
    })

    assert b'Length of username should be 8 to 12 characters' in response.data

# test for registration with passwords that do not match
def test_register_password_not_matching(client):
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'username': "testuser",
        'password': 'password',
        'confirm_password': 'password1'
    })

    assert b'Passwords do not match' in response.data
