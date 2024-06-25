import unittest
from app import create_app, db
from app.models.white_label import WhiteLabel
from app.models.user import User

class WhiteLabelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        self.white_label = WhiteLabel(name='Test White Label', user_id=self.user.id)
        db.session.add(self.white_label)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_white_label(self):
        response = self.client.post('/white_label', data={
            'name': 'New Test White Label',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'White label created successfully.', response.data)

    def test_get_white_label(self):
        response = self.client.get(f'/white_label/{self.white_label.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test White Label', response.data)

    def test_update_white_label(self):
        response = self.client.put(f'/white_label/{self.white_label.id}', data={
            'name': 'Updated Test White Label'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'White label updated successfully.', response.data)

    def test_delete_white_label(self):
        response = self.client.delete(f'/white_label/{self.white_label.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'White label deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
