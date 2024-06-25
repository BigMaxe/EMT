import unittest
from app import create_app, db
from app.models.integration import Integration
from app.models.user import User

class IntegrationsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        # Add a test user
        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        # Add a test integration
        self.integration = Integration(name='Test Integration', type='API', user_id=self.user.id)
        db.session.add(self.integration)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_integration(self):
        response = self.client.post('/integrations', data={
            'name': 'New Integration',
            'type': 'Webhook',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Integration created successfully.', response.data)

    def test_get_integration(self):
        response = self.client.get(f'/integrations/{self.integration.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Integration', response.data)

    def test_update_integration(self):
        response = self.client.put(f'/integrations/{self.integration.id}', data={
            'name': 'Updated Integration',
            'type': 'API'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Integration updated successfully.', response.data)

    def test_delete_integration(self):
        response = self.client.delete(f'/integrations/{self.integration.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Integration deleted successfully.', response.data)

    def test_get_all_integrations(self):
        integration2 = Integration(name='Another Integration', type='API', user_id=self.user.id)
        db.session.add(integration2)
        db.session.commit()

        response = self.client.get('/integrations')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Integration', response.data)
        self.assertIn(b'Another Integration', response.data)

if __name__ == '__main__':
    unittest.main()
