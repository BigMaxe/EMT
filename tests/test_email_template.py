import unittest
from app import create_app, db
from app.models.email_template import EmailTemplate
from app.models.user import User

class EmailTemplateTestCase(unittest.TestCase):

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

    def test_create_email_template(self):
        response = self.client.post('/email_template', data={
            'name': 'Test Template',
            'subject': 'Test Subject',
            'body': 'This is a test email template.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Email template created successfully.', response.data)

    def test_get_email_template(self):
        email_template = EmailTemplate(name='Test Template', subject='Test Subject', body='This is a test email template.', user_id=self.user.id)
        db.session.add(email_template)
        db.session.commit()

        response = self.client.get(f'/email_template/{email_template.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Template', response.data)

    def test_update_email_template(self):
        email_template = EmailTemplate(name='Test Template', subject='Test Subject', body='This is a test email template.', user_id=self.user.id)
        db.session.add(email_template)
        db.session.commit()

        response = self.client.put(f'/email_template/{email_template.id}', data={
            'name': 'Updated Test Template',
            'subject': 'Updated Test Subject',
            'body': 'This is an updated test email template.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email template updated successfully.', response.data)

    def test_delete_email_template(self):
        email_template = EmailTemplate(name='Test Template', subject='Test Subject', body='This is a test email template.', user_id=self.user.id)
        db.session.add(email_template)
        db.session.commit()

        response = self.client.delete(f'/email_template/{email_template.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email template deleted successfully.', response.data)

    def test_get_all_email_templates(self):
        email_template1 = EmailTemplate(name='Test Template 1', subject='Test Subject 1', body='This is test email template 1.', user_id=self.user.id)
        email_template2 = EmailTemplate(name='Test Template 2', subject='Test Subject 2', body='This is test email template 2.', user_id=self.user.id)
        db.session.add(email_template1)
        db.session.add(email_template2)
        db.session.commit()

        response = self.client.get('/email_templates')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Template 1', response.data)
        self.assertIn(b'Test Template 2', response.data)

if __name__ == '__main__':
    unittest.main()
