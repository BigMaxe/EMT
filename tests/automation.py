import unittest
from app import create_app, db
from app.models import User, Automation

class AutomationTestCase(unittest.TestCase):

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_automation(self):
        response = self.client.post('/automation', data={
            'name': 'Test Automation',
            'description': 'This is a test automation.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Automation created successfully.', response.data)

    def test_get_automation(self):
        automation = Automation(name='Test Automation', description='This is a test automation.', user_id=self.user.id)
        db.session.add(automation)
        db.session.commit()

        response = self.client.get(f'/automation/{automation.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Automation', response.data)

    def test_update_automation(self):
        automation = Automation(name='Test Automation', description='This is a test automation.', user_id=self.user.id)
        db.session.add(automation)
        db.session.commit()

        response = self.client.put(f'/automation/{automation.id}', data={
            'name': 'Updated Automation',
            'description': 'This is an updated test automation.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Automation updated successfully.', response.data)

    def test_delete_automation(self):
        automation = Automation(name='Test Automation', description='This is a test automation.', user_id=self.user.id)
        db.session.add(automation)
        db.session.commit()

        response = self.client.delete(f'/automation/{automation.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Automation deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
