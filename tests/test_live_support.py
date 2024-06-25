import unittest
from app import create_app, db
from app.models.live_support import LiveSupport
from app.models.user import User

class LiveSupportTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        self.live_support = LiveSupport(message='Test Message', user_id=self.user.id)
        db.session.add(self.live_support)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_live_support(self):
        response = self.client.post('/live_support', data={
            'message': 'New Test Message',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Live support message created successfully.', response.data)

    def test_get_live_support(self):
        response = self.client.get(f'/live_support/{self.live_support.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Message', response.data)

    def test_update_live_support(self):
        response = self.client.put(f'/live_support/{self.live_support.id}', data={
            'message': 'Updated Test Message'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live support message updated successfully.', response.data)

    def test_delete_live_support(self):
        response = self.client.delete(f'/live_support/{self.live_support.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live support message deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
