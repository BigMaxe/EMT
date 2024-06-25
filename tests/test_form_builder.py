import unittest
from app import create_app, db
from app.models.form_response import FormResponse
from app.models.user import User
from app.models.question import Question

class FormBuilderTestCase(unittest.TestCase):

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

    def test_create_form(self):
        response = self.client.post('/form_builder/save_form', data={
            'form_name': 'Test Form',
            'description': 'This is a test form.',
            'user_id': self.user.id,
            'questions': [
                {
                    'question_text': 'What is your name?',
                    'question_type': 'text'
                },
                {
                    'question_text': 'How old are you?',
                    'question_type': 'number'
                }
            ]
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Form created successfully.', response.data)

    def test_get_form(self):
        form_response = FormResponse(form_name='Test Form', description='This is a test form.', user_id=self.user.id)
        db.session.add(form_response)
        db.session.commit()

        response = self.client.get(f'/form_builder/{form_response.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Form', response.data)

    def test_update_form(self):
        form_response = FormResponse(form_name='Test Form', description='This is a test form.', user_id=self.user.id)
        db.session.add(form_response)
        db.session.commit()

        response = self.client.put(f'/form_builder/{form_response.id}', data={
            'form_name': 'Updated Test Form',
            'description': 'This is an updated test form.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Form updated successfully.', response.data)

    def test_delete_form(self):
        form_response = FormResponse(form_name='Test Form', description='This is a test form.', user_id=self.user.id)
        db.session.add(form_response)
        db.session.commit()

        response = self.client.delete(f'/form_builder/{form_response.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Form deleted successfully.', response.data)

    def test_get_all_forms(self):
        form_response1 = FormResponse(form_name='Test Form 1', description='This is test form 1.', user_id=self.user.id)
        form_response2 = FormResponse(form_name='Test Form 2', description='This is test form 2.', user_id=self.user.id)
        db.session.add(form_response1)
        db.session.add(form_response2)
        db.session.commit()

        response = self.client.get('/form_builder')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Form 1', response.data)
        self.assertIn(b'Test Form 2', response.data)

if __name__ == '__main__':
    unittest.main()
