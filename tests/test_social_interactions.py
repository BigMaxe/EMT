import unittest
from app import create_app, db
from app.models.social_interactions import SocialInteractions
from app.models.user import User

class SocialInteractionsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        self.social_interactions = SocialInteractions(interaction='Test Interaction', user_id=self.user.id)
        db.session.add(self.social_interactions)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_social_interaction(self):
        response = self.client.post('/social_interactions', data={
            'interaction': 'New Test Interaction',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Social interaction created successfully.', response.data)

    def test_get_social_interaction(self):
        response = self.client.get(f'/social_interactions/{self.social_interactions.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Interaction', response.data)

    def test_update_social_interaction(self):
        response = self.client.put(f'/social_interactions/{self.social_interactions.id}', data={
            'interaction': 'Updated Test Interaction'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Social interaction updated successfully.', response.data)

    def test_delete_social_interaction(self):
        response = self.client.delete(f'/social_interactions/{self.social_interactions.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Social interaction deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
