import unittest
import json
from app import app

class DailyHoroscopeTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_daily_horoscope(self):
        response = self.app.post('/api/daily-horoscope', json={
            'sign': 'leo',
            'day': 'TODAY'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)

if __name__ == '__main__':
    unittest.main()
