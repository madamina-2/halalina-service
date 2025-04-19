import unittest
from flask_jwt_extended import create_refresh_token
from werkzeug.security import generate_password_hash
from app import create_app 
from app.models.user import User
from unittest.mock import patch
import json

class TestAuthBlueprint(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a test app
        self.app = create_app()
        self.client = self.app.test_client()

        # Set up any needed configuration here (e.g., for testing)
        self.app.config['TESTING'] = True
        self.app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.create')
    def test_register_success(self, mock_create, mock_get_user_by_email):
        """Test successful user registration"""
        mock_get_user_by_email.return_value = None  # simulate email not in DB
        mock_create.return_value = User(id=1, full_name="Test User", email="testuser@example.com", password_hash="hashedpassword", phone_number="08123456789")

        # Prepare test data
        data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'Password123!',
            'phone_number': '08123456789'
        }

        # Send POST request to register endpoint
        response = self.client.post('/auth/register', json=data)

        # Assert response status and content
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data['data'])
        self.assertIn('refresh_token', response_data['data'])

    @patch('app.models.user.User.get_user_by_email')
    def test_register_email_already_exists(self, mock_get_user_by_email):
        """Test registration where email already exists"""
        mock_get_user_by_email.return_value = User(id=1, full_name="Test User", email="testuser@example.com", password_hash="hashedpassword", phone_number="08123456789")

        # Prepare test data
        data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'Password123!',
            'phone_number': '08123456789'
        }

        # Send POST request to register endpoint
        response = self.client.post('/auth/register', json=data)

        # Assert response status and content
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], "Email sudah terdaftar")

    @patch('app.models.user.User.get_user_by_email')
    def test_login_success(self, mock_get_user_by_email):
        """Test login success"""
        mock_get_user_by_email.return_value = User(id=1, full_name="Test User", email="testuser@example.com", password_hash=generate_password_hash("Password123!"), phone_number="08123456789")
        # Prepare test data
        data = {
            'email': 'testuser@example.com',
            'password': 'Password123!'
        }

        # Send POST request to login endpoint
        response = self.client.post('/auth/login', json=data)

        # Print the response for debugging purposes
        if response.status_code != 200:
            print(response.data)  # To see the error message when it's 400
        # Assert response status and content
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data['data'])
        self.assertIn('refresh_token', response_data['data'])

    @patch('app.models.user.User.get_user_by_email')
    def test_login_invalid_credentials(self, mock_get_user_by_email):
        """Test login with invalid credentials"""
        mock_get_user_by_email.return_value = None  # simulate email not in DB

        # Prepare test data
        data = {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        }

        # Send POST request to login endpoint
        response = self.client.post('/auth/login', json=data)

        # Assert response status and content
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], "Email atau password salah")

    @patch('app.models.user.User.get_user_by_email')
    @patch('app.models.user.User.create')
    def test_refresh_token(self, mock_create, mock_get_user_by_email):
        with self.app.app_context():
            """Test refresh token"""
            mock_get_user_by_email.return_value = User(id=1, full_name="Test User", email="testuser@example.com", password_hash="hashedpassword", phone_number="08123456789")
            mock_create.return_value = User(id=1, full_name="Test User", email="testuser@example.com", password_hash="hashedpassword", phone_number="08123456789")

            # Generate a refresh token (assuming a valid JWT token is required for this endpoint)
            refresh_token = create_refresh_token(identity=1)

            # Send POST request to refresh endpoint with the refresh token
            response = self.client.post(
                '/auth/refresh',
                headers={'Authorization': f'Bearer {refresh_token}'}
            )

            # Assert response status and content
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertIn('access_token', response_data['data'])

if __name__ == '__main__':
    unittest.main()
