import unittest
from app import create_app, db
from app.models.campaign import Campaign
from app.models.user import User

class CampaignTestCase(unittest.TestCase):

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

    def test_create_campaign(self):
        response = self.client.post('/campaign', data={
            'name': 'Test Campaign',
            'subject': 'Test Subject',
            'body': 'This is a test campaign.',
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Campaign created successfully.', response.data)

    def test_get_campaign(self):
        campaign = Campaign(name='Test Campaign', subject='Test Subject', body='This is a test campaign.', user_id=self.user.id)
        db.session.add(campaign)
        db.session.commit()

        response = self.client.get(f'/campaign/{campaign.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Campaign', response.data)

    def test_update_campaign(self):
        campaign = Campaign(name='Test Campaign', subject='Test Subject', body='This is a test campaign.', user_id=self.user.id)
        db.session.add(campaign)
        db.session.commit()

        response = self.client.put(f'/campaign/{campaign.id}', data={
            'name': 'Updated Test Campaign',
            'subject': 'Updated Test Subject',
            'body': 'This is an updated test campaign.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Campaign updated successfully.', response.data)

    def test_delete_campaign(self):
        campaign = Campaign(name='Test Campaign', subject='Test Subject', body='This is a test campaign.', user_id=self.user.id)
        db.session.add(campaign)
        db.session.commit()

        response = self.client.delete(f'/campaign/{campaign.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Campaign deleted successfully.', response.data)

    def test_get_all_campaigns(self):
        campaign1 = Campaign(name='Test Campaign 1', subject='Test Subject 1', body='This is test campaign 1.', user_id=self.user.id)
        campaign2 = Campaign(name='Test Campaign 2', subject='Test Subject 2', body='This is test campaign 2.', user_id=self.user.id)
        db.session.add(campaign1)
        db.session.add(campaign2)
        db.session.commit()

        response = self.client.get('/campaigns')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Campaign 1', response.data)
        self.assertIn(b'Test Campaign 2', response.data)

if __name__ == '__main__':
    unittest.main()
