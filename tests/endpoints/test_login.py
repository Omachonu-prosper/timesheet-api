import unittest
import requests
import json
import string
import random
import tests.helpers as helpers


"""
Test function to test /user/login

Test cases
- Requests with incomplete payload
- Correct email with wrong password
- Correct password wrong email
- Correct credentials
"""
class TestLogin(unittest.TestCase):
    url = 'http://localhost:5000/user/login'
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json'
    }


    def setUp(self):
        self.user = helpers.return_db_user()
        helpers.activate_user(self.user['_id'])


    def test_incomplete_payload(self):
        req_without_passwd = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({ 'email': self.user['email'] }
        ))
        req_without_email = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({ 'password': self.user['password'] }
        ))
        self.assertEqual(req_without_passwd.status_code, 400)
        self.assertEqual(req_without_email.status_code, 400)
        self.assertFalse(req_without_passwd.json()['status'])
        self.assertFalse(req_without_email.json()['status'])


    def test_correct_email(self):
        req = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({
                'email': self.user['email'],
                'password': 'wrong-password'
            }
        ))
        self.assertEqual(req.status_code, 401)
        self.assertFalse(req.json()['status'])


    def test_correct_passwd(self):
        req = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({
                'email': 'wrong-email',
                'password': self.user['password']
            }
        ))
        self.assertEqual(req.status_code, 404)
        self.assertFalse(req.json()['status'])


    def test_correct_credentials(self):
        req = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps({
                'email': self.user['email'],
                'password': self.user['password']
            }
        ))
        self.assertEqual(req.status_code, 200)
        self.assertTrue(req.json()['status'])
        self.assertIsNotNone(req.json()['access_token'])
        self.assertIsNotNone(req.json()['message'])
        self.assertIsNotNone(req.json()['user-id'])


    def tearDown(self):
        helpers.delete_user(self.user['_id'])
