import unittest
import requests
import os

from dotenv import load_dotenv

# Load all environment variables
load_dotenv()

class TestRoutes(unittest.TestCase):
    def test_index(self):
        """
        Test function to test '/' route

        - On success a 200 status code is returned
        - If no API key is sent with the request or a wrong API key is sent
            the appropriate error message and HTTP status code is returned in the response
        - On failure (service is down) a 500 error code is returned
        """
        url = 'http://127.0.0.1:5000/'
        correct_headers = {
            'x-api-key': os.environ.get('API_KEY', None)
        }
        wrong_headers = {
            'x-api-key': 'wrong-key'
        }

        request_without_header = requests.get(url=url)
        request_with_wrong_header = requests.get(url=url, headers=wrong_headers)
        request_with_header = requests.get(url=url, headers=correct_headers)
        
        # The request sent without a header should return a status code of 400
        self.assertEqual(request_without_header.status_code, 400)
        # The request sent with a wrong header should return a status code of 401
        self.assertEqual(request_with_wrong_header.status_code, 401)
        # The request sent with a header should return a status code of 200
        self.assertEqual(request_with_header.status_code, 200)
        
