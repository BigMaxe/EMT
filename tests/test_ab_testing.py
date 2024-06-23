import unittest
from app import create_app, db
from app.models.ab_testing import ABTest, ABTestResult
from app.models.user import User

class ABTestingTestCase(unittest.TestCase):

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

    def test_create_ab_test(self):
        response = self.client.post('/ab_testing', data={
            'name': 'Test AB',
            'description': 'This is a test A/B test.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'AB Test created successfully.', response.data)

    def test_get_ab_test(self):
        ab_test = ABTest(name='Test AB', description='This is a test A/B test.', user_id=self.user.id)
        db.session.add(ab_test)
        db.session.commit()

        response = self.client.get(f'/ab_testing/{ab_test.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test AB', response.data)

    def test_update_ab_test(self):
        ab_test = ABTest(name='Test AB', description='This is a test A/B test.', user_id=self.user.id)
        db.session.add(ab_test)
        db.session.commit()

        response = self.client.put(f'/ab_testing/{ab_test.id}', data={
            'name': 'Updated AB Test',
            'description': 'This is an updated test A/B test.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AB Test updated successfully.', response.data)

    def test_delete_ab_test(self):
        ab_test = ABTest(name='Test AB', description='This is a test A/B test.', user_id=self.user.id)
        db.session.add(ab_test)
        db.session.commit()

        response = self.client.delete(f'/ab_testing/{ab_test.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AB Test deleted successfully.', response.data)

    def test_create_ab_test_result(self):
        ab_test = ABTest(name='Test AB', description='This is a test A/B test.', user_id=self.user.id)
        db.session.add(ab_test)
        db.session.commit()

        response = self.client.post(f'/ab_testing/{ab_test.id}/results', data={
            'variant': 'A',
            'conversion': True,
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'AB Test result recorded successfully.', response.data)

    def test_get_ab_test_results(self):
        ab_test = ABTest(name='Test AB', description='This is a test A/B test.', user_id=self.user.id)
        db.session.add(ab_test)
        db.session.commit()

        ab_test_result = ABTestResult(variant='A', conversion=True, user_id=self.user.id, ab_test_id=ab_test.id)
        db.session.add(ab_test_result)
        db.session.commit()

        response = self.client.get(f'/ab_testing/{ab_test.id}/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"variant": "A"', response.data)

if __name__ == '__main__':
    unittest.main()
