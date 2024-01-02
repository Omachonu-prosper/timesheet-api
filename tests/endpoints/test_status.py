import unittest
import tests.helpers as helpers
import requests

"""
Test Class for the status api endpoint

Test cases
- Correct response
"""
class TestAPIStatus(unittest.TestCase):
    url = 'http://127.0.0.1:5000/api/status'
    headers = {
        'x-api-key': helpers.API_KEY
    }


    def test_correct_response(self):
        req = requests.get(
            url=self.url,
            headers=self.headers
        )

        self.assertEqual(req.status_code, 200)
        self.assertEqual(
            req.json()['message'],
            'API is healthy and running'
        )
        self.assertTrue(req.json()['status'])