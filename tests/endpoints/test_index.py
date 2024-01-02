import unittest
import requests
import tests.helpers as helpers


"""
Test function to test '/' route

Test cases
- On success
- No API key is sent
- Wrong ApI key is sent
"""
class TestIndex(unittest.TestCase):
    url = 'http://127.0.0.1:5000/'
    correct_headers = {
        'x-api-key': helpers.API_KEY
    }
    wrong_headers = {
        'x-api-key': 'wrong-key'
    }

    def test_on_success(self):
        req = requests.get(
            url=self.url,
            headers=self.correct_headers
        )
        self.assertEqual(req.status_code, 200)

    def test_no_key(self):
        req = requests.get(url=self.url)
        self.assertEqual(req.status_code, 400)

    def test_wrong_key(self):
        req = requests.get(
            url=self.url,
            headers=self.wrong_headers
        )
        self.assertEqual(req.status_code, 401)