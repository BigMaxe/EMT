import unittest
from app import create_app, db
from app.models.scheduling import Scheduling
from app.models.user import User

class SchedulingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        self.scheduling = Scheduling(event='Test Event', user_id=self.user.id)
        db.session.add(self.scheduling)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_scheduling(self):
        response = self.client.post('/scheduling', data={
            'event': 'New Test Event',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Scheduling event created successfully.', response.data)

    def test_get_scheduling(self):
        response = self.client.get(f'/scheduling/{self.scheduling.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Event', response.data)

    def test_update_scheduling(self):
        response = self.client.put(f'/scheduling/{self.scheduling.id}', data={
            'event': 'Updated Test Event'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Scheduling event updated successfully.', response.data)

    def test_delete_scheduling(self):
        response = self.client.delete(f'/scheduling/{self.scheduling.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Scheduling event deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
