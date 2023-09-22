import unittest
from unittest.mock import patch, MagicMock
from app import app

class LoginTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        
    def tearDown(self):
        pass
    
    def test_login_success(self):
        # Mock the database connection and cursor objects
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        cur.fetchone.return_value = ('testuser', 'Test User', 'password', 'testuser@example.com', '2023-05-04 19:55:01')

        # Send a POST request with valid credentials
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'password'})

        # Check that the response redirects to the dashboard page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/dashboard')
        
        # Check that the session contains the username
        with self.app.session_transaction() as session:
            self.assertEqual(session['username'], 'testuser')
        
    def test_login_invalid_credentials(self):
        # Mock the database connection and cursor objects
        conn = MagicMock()
        cur = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        cur.fetchone.return_value = None

        # Send a POST request with invalid credentials
        response = self.app.post('/login', data={'username': 'username', 'password': 'password'})

        # Check that the response contains an error message
        self.assertIn(b'Invalid credentials', response.data)
