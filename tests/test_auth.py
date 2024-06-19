# tests/test_auth.py
import unittest
import json
from app import app, db
from app.models.user import User
from app.config import config

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        rv = self.app.post('/register', data=json.dumps({
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'password'
        }), content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        self.assertIn(b'User created successfully', rv.data)

    def test_login(self):
        new_user = User(username='test_user', email='test@example.com')
        new_user.set_password('password')
        db.session.add(new_user)
        db.session.commit()

        rv = self.app.post('/login', data=json.dumps({
            'username': 'test_user',
            'password': 'password'
        }), content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Login successful', rv.data)

    def test_login_invalid_credentials(self):
        rv = self.app.post('/login', data=json.dumps({
            'username': 'non_existing_user',
            'password': 'password'
        }), content_type='application/json')
        self.assertEqual(rv.status_code, 401)
        self.assertIn(b'Invalid username or password', rv.data)

if __name__ == '__main__':
    unittest.main()
