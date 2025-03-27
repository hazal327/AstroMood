import unittest
import json
from pathlib import Path
from app import app

class FeedbackSystemTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.feedback_file = Path(__file__).parent.parent / "test_feedback.json"
        
        if self.feedback_file.exists():
            self.feedback_file.unlink()

    def tearDown(self):
        if self.feedback_file.exists():
            self.feedback_file.unlink()

    def test_feedback_flow(self):
        # Test rating submission
        for rating in [5, 3, 4]:
            response = self.app.post('/submit_rating', json={'rating': rating})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['success'])

        # Test statistics
        response = self.app.get('/get_rating_stats')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['average'], 4.0)
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['counts'], {'1':0, '2':0, '3':1, '4':1, '5':1})

if __name__ == '__main__':
    unittest.main()
