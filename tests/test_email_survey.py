import unittest
from app import create_app, db
from app.models.email_survey import EmailSurvey
from app.models.user import User

class EmailSurveyTestCase(unittest.TestCase):

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

    def test_create_email_survey(self):
        response = self.client.post('/email_survey', data={
            'title': 'Test Survey',
            'description': 'This is a test survey.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Email survey created successfully.', response.data)

    def test_get_email_survey(self):
        email_survey = EmailSurvey(title='Test Survey', description='This is a test survey.', user_id=self.user.id)
        db.session.add(email_survey)
        db.session.commit()

        response = self.client.get(f'/email_survey/{email_survey.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Survey', response.data)

    def test_update_email_survey(self):
        email_survey = EmailSurvey(title='Test Survey', description='This is a test survey.', user_id=self.user.id)
        db.session.add(email_survey)
        db.session.commit()

        response = self.client.put(f'/email_survey/{email_survey.id}', data={
            'title': 'Updated Test Survey',
            'description': 'This is an updated test survey.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email survey updated successfully.', response.data)

    def test_delete_email_survey(self):
        email_survey = EmailSurvey(title='Test Survey', description='This is a test survey.', user_id=self.user.id)
        db.session.add(email_survey)
        db.session.commit()

        response = self.client.delete(f'/email_survey/{email_survey.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email survey deleted successfully.', response.data)

    def test_get_all_email_surveys(self):
        email_survey1 = EmailSurvey(title='Test Survey 1', description='This is test survey 1.', user_id=self.user.id)
        email_survey2 = EmailSurvey(title='Test Survey 2', description='This is test survey 2.', user_id=self.user.id)
        db.session.add(email_survey1)
        db.session.add(email_survey2)
        db.session.commit()

        response = self.client.get('/email_surveys')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Survey 1', response.data)
        self.assertIn(b'Test Survey 2', response.data)

if __name__ == '__main__':
    unittest.main()
