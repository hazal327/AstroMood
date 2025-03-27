import unittest
import json
from app import app

class MovieRecommendationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_movie_recommendation(self):
        response = self.app.post('/get_movie', json={
            'mood': 'stressed',
            'zodiac': 'taurus'
        })
        data = json.loads(response.data)
        self.assertIn('title', data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
