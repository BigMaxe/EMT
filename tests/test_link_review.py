import unittest
from app import create_app, db
from app.models.link_review import LinkReview
from app.models.user import User

class LinkReviewTestCase(unittest.TestCase):

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

        # Add a test link review
        self.link_review = LinkReview(url='http://example.com', comment='Test Comment', user_id=self.user.id)
        db.session.add(self.link_review)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_link_review(self):
        response = self.client.post('/link_reviews', data={
            'url': 'http://newexample.com',
            'comment': 'New Comment',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Link review created successfully.', response.data)

    def test_get_link_review(self):
        response = self.client.get(f'/link_reviews/{self.link_review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Comment', response.data)

    def test_update_link_review(self):
        response = self.client.put(f'/link_reviews/{self.link_review.id}', data={
            'url': 'http://updatedexample.com',
            'comment': 'Updated Comment'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Link review updated successfully.', response.data)

    def test_delete_link_review(self):
        response = self.client.delete(f'/link_reviews/{self.link_review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Link review deleted successfully.', response.data)

    def test_get_all_link_reviews(self):
        link_review2 = LinkReview(url='http://anotherexample.com', comment='Another Comment', user_id=self.user.id)
        db.session.add(link_review2)
        db.session.commit()

        response = self.client.get('/link_reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Comment', response.data)
        self.assertIn(b'Another Comment', response.data)

if __name__ == '__main__':
    unittest.main()
