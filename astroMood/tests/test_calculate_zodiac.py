import unittest
import json
from app import app

class CalculateZodiacTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_valid_zodiac(self):
        test_cases = [
            (20, 1, "aquarius"),
            (19, 2, "pisces"),
            (21, 3, "aries")
        ]
        
        for day, month, expected in test_cases:
            with self.subTest(day=day, month=month):
                response = self.app.post('/api/calculate-zodiac', json={
                    'day': day,
                    'month': month
                })
                data = json.loads(response.data)
                self.assertEqual(data['zodiac_en'], expected)
                self.assertEqual(response.status_code, 200)

    def test_invalid_zodiac(self):
        response = self.app.post('/api/calculate-zodiac', json={
            'day': 32,
            'month': 13
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
