import unittest
import psycopg2
import os
from dash import dcc
from app import app
import pytest
from dash.dependencies import Input, Output
from dotenv import load_dotenv
load_dotenv()
from app import create_dashapp
import pandas as pd
from preprocess import data_filtering_trendchart

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_successful(self):
        response = self.app.post('/login', data=dict(
            username="admin_login",
            password="password"
        ))
        self.assertEqual(response.status_code, 302) # expect redirect to dashboard page

    def test_login_unsuccessful(self):
        response = self.app.post('/login', data=dict(
            username="invalid_user",
            password="invalid_password"
        ))
        self.assertIn(b"Invalid credentials", response.data) # expect error message

    # def test_register_successful(self):
    #     response = self.app.post('/register', data=dict(
    #         name="Test User",
    #         email="test_user@example.com",
    #         username="test_user",
    #         password="test_password",
    #         confirm_password="test_password"
    #     ))
    #     self.assertEqual(response.status_code, 302) # expect redirect to dashboard page

    def test_register_invalid_email(self):
        response = self.app.post('/register', data=dict(
            name="Test User",
            email="invalid_email",
            username="test_user",
            password="test_password",
            confirm_password="test_password"
        ))
        self.assertIn(b"Invalid email address", response.data) # expect error message

    def test_register_invalid_username_length(self):
        response = self.app.post('/register', data=dict(
            name="Test User",
            email="test_user@example.com",
            username="short",
            password="test_password",
            confirm_password="test_password"
        ))
        self.assertIn(b"Length of username should be 8 to 12 characters", response.data) # expect error message

    def test_register_passwords_do_not_match(self):
        response = self.app.post('/register', data=dict(
            name="Test User",
            email="test_user@example.com",
            username="test_user",
            password="test_password",
            confirm_password="wrong_password"
        ))
        self.assertIn(b"Passwords do not match", response.data) # expect error message

    def test_dashboard_without_login(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302) # expect redirect to login page

    def test_dashboard_with_login(self):
        with self.app.session_transaction() as session:
            session['username'] = 'test_user'
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200) # expect successful page load

    def test_logout(self):
        with self.app.session_transaction() as session:
            session['username'] = 'test_user'
        response = self.app.get('/logout')
        with self.app.session_transaction() as session:
            self.assertNotIn('username', session) # expect session to be cleared
        self.assertEqual(response.status_code, 302) # expect redirect to login page
            
    def test_about(self):
        with self.app:
            response = self.app.get('/about')
            self.assertEqual(response.status_code, 200)
            
    def test_contacts(self):
        with self.app:
            response = self.app.get('/contacts')
            self.assertEqual(response.status_code, 200)
    
    def test_denver(self):
        with self.app:
            response = self.app.get('/denver')
            self.assertEqual(response.status_code, 200)
    
    def test_reports(self):
        with self.app:
            response = self.app.get('/dash/')
            self.assertEqual(response.status_code, 200)
    
            
    # def test_tab_content(self):
    #     # Test case 1: active_tab is tab-1
    #     active_tab = "tab-1"
    #     expected_output = dcc.Graph(id="treemap", style={'border-width': '0', 'width': '125%', 'height': '1000px', 'margin-left': '-13%'})
    #     assert create_dashapp.tab_content(active_tab) == expected_output

    #     # Test case 2: active_tab is tab-2
    #     active_tab = "tab-2"
    #     expected_output = dcc.Graph(id="treemap_2", style={'border-width': '0', 'width': '125%', 'height': '1000px', 'margin-left': '-13%'})
    #     assert create_dashapp.tab_content(active_tab) == expected_output

    #     # Test case 3: active_tab is invalid
    #     active_tab = "tab-3"
    #     expected_output = None
    #     assert create_dashapp.tab_content(active_tab) == expected_output
            
# class TestData(unittest.TestCase):
    
#     def test_data_filtering_trendchart(self):
        
#         # Test with valid inputs
#         state = ['California', 'Texas']
#         crime = ['Arson', 'Assault Offenses']
#         metric = 'total'
#         year_range = [2010, 2015]
#         data_crime = pd.DataFrame({
#             'State': ['California', 'Texas', 'New York', 'Florida'],
#             'Arson': [200, 300, 400, 500],
#             'Assault Offenses': [600, 700, 800, 900],
#             'year': [2010, 2011, 2012, 2015]
#         })
#         expected_output = pd.DataFrame({
#             'State': ['California', 'Texas'],
#             'crime_count': [1200, 1700],
#             'population': [30000000, 25000000]
#         })
#         result = data_filtering_trendchart(state, crime, metric, year_range, data_crime)
#         pd.testing.assert_frame_equal(result, expected_output)
        
#         # Test with empty inputs
#         state = []
#         crime = []
#         metric = 'per_capita'
#         year_range = None
#         data_crime = pd.DataFrame()
#         expected_output = pd.DataFrame(columns=['State', 'crime_count', 'population'])
#         result = data_filtering_trendchart(state, crime, metric, year_range, data_crime)
#         pd.testing.assert_frame_equal(result, expected_output)
        
#         # Test with invalid inputs
#         state = ['Florida', 'Alabama']
#         crime = ['Robbery', 'Burglary']
#         metric = 'invalid_metric'
#         year_range = [2000, 2010]
#         data_crime = pd.DataFrame({
#             'State': ['California', 'Texas', 'New York', 'Florida'],
#             'Robbery': [100, 200, 300, 400],
#             'Burglary': [500, 600, 700, 800],
#             'year': [2010, 2011, 2012, 2015]
#         })
#         expected_output = pd.DataFrame(columns=['State', 'crime_count', 'population'])
#         result = data_filtering_trendchart(state, crime, metric, year_range, data_crime)
#         pd.testing.assert_frame_equal(result, expected_output)

if __name__ == '__main__':
    unittest.main()