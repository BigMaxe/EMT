import unittest
from app import create_app, db
from app.models.email_list import EmailList
from app.models.user import User

class EmailListTestCase(unittest.TestCase):

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

    def test_create_email_list(self):
        response = self.client.post('/email_list', data={
            'name': 'Test Email List',
            'description': 'This is a test email list.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Email list created successfully.', response.data)

    def test_get_email_list(self):
        email_list = EmailList(name='Test Email List', description='This is a test email list.', user_id=self.user.id)
        db.session.add(email_list)
        db.session.commit()

        response = self.client.get(f'/email_list/{email_list.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Email List', response.data)

    def test_update_email_list(self):
        email_list = EmailList(name='Test Email List', description='This is a test email list.', user_id=self.user.id)
        db.session.add(email_list)
        db.session.commit()

        response = self.client.put(f'/email_list/{email_list.id}', data={
            'name': 'Updated Test Email List',
            'description': 'This is an updated test email list.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email list updated successfully.', response.data)

    def test_delete_email_list(self):
        email_list = EmailList(name='Test Email List', description='This is a test email list.', user_id=self.user.id)
        db.session.add(email_list)
        db.session.commit()

        response = self.client.delete(f'/email_list/{email_list.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email list deleted successfully.', response.data)

    def test_get_all_email_lists(self):
        email_list1 = EmailList(name='Test Email List 1', description='This is test email list 1.', user_id=self.user.id)
        email_list2 = EmailList(name='Test Email List 2', description='This is test email list 2.', user_id=self.user.id)
        db.session.add(email_list1)
        db.session.add(email_list2)
        db.session.commit()

        response = self.client.get('/email_lists')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Email List 1', response.data)
        self.assertIn(b'Test Email List 2', response.data)

if __name__ == '__main__':
    unittest.main()
