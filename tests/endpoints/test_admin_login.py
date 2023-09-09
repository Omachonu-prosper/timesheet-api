import unittest
import requests
import helpers
import json


class TestAdminLogin(unittest.TestCase):
    """
    Test class to test admin login '/admin/login'

    Test cases
    - Incomplete payload
    - Incorrect credentials
    - Correct credentials
    """

    url = 'http://127.0.0.1:5000/admin/login'
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json'
    }

    def test_incomplete_payload(self):
        """
        Workflow
        - Send request with only username as payload
        - Send request with only password as payload
        - Test that the response is as expected
        """
        
        req_email = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({
                'username': 'admin-username'
            })
        )
        req_password = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({
                'password': 'admin-password'
            })
        )

        self.assertEqual(
            req_email.json()['message'],
            'Missing required parameter'
        )
        self.assertEqual(req_email.status_code, 400)
        self.assertFalse(req_email.json()['status'])
        self.assertEqual(
            req_password.json()['message'],
            'Missing required parameter'
        )
        self.assertEqual(req_password.status_code, 400)
        self.assertFalse(req_password.json()['status'])

    def test_incorrect_credentials(self):
        pass

    def test_correct_credentials(self):
        pass
