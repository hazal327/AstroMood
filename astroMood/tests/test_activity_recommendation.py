import unittest
import json
from app import app

class ActivityRecommendationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_activity_recommendation(self):
        response = self.app.post('/get_activity', json={
            'mood': 'happy',
            'zodiac': 'leo'
        })
        data = json.loads(response.data)
        self.assertIn('activity', data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
