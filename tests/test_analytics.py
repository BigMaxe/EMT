import unittest
from app import create_app, db
from app.models.analytics import AnalyticsEvent
from app.models.user import User

class AnalyticsTestCase(unittest.TestCase):

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

    def test_create_analytics_event(self):
        response = self.client.post('/analytics', data={
            'event_name': 'Test Event',
            'event_data': 'This is test data.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Analytics event created successfully.', response.data)

    def test_get_analytics_event(self):
        event = AnalyticsEvent(event_name='Test Event', event_data='This is test data.', user_id=self.user.id)
        db.session.add(event)
        db.session.commit()

        response = self.client.get(f'/analytics/{event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Event', response.data)

    def test_update_analytics_event(self):
        event = AnalyticsEvent(event_name='Test Event', event_data='This is test data.', user_id=self.user.id)
        db.session.add(event)
        db.session.commit()

        response = self.client.put(f'/analytics/{event.id}', data={
            'event_name': 'Updated Test Event',
            'event_data': 'This is updated test data.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analytics event updated successfully.', response.data)

    def test_delete_analytics_event(self):
        event = AnalyticsEvent(event_name='Test Event', event_data='This is test data.', user_id=self.user.id)
        db.session.add(event)
        db.session.commit()

        response = self.client.delete(f'/analytics/{event.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analytics event deleted successfully.', response.data)

    def test_get_all_analytics_events(self):
        event1 = AnalyticsEvent(event_name='Test Event 1', event_data='This is test data 1.', user_id=self.user.id)
        event2 = AnalyticsEvent(event_name='Test Event 2', event_data='This is test data 2.', user_id=self.user.id)
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()

        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Event 1', response.data)
        self.assertIn(b'Test Event 2', response.data)

if __name__ == '__main__':
    unittest.main()
