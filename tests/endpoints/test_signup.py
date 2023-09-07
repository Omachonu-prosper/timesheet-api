import unittest
import requests
import json
import string
import random
import helpers


"""
Test function to test /user/signup

Test Cases
- Incomplete payload
- Duplicate credentials
- On success
"""
class TestSignup(unittest.TestCase):
    url = 'http://127.0.0.1:5000/user/signup'
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json'
    }

    # Generate random strings to be used as test data
    firstname = ''.join(random.choices(
        string.ascii_lowercase,
        k=random.randint(5, 10)
    ))
    lastname = ''.join(random.choices(
        string.ascii_lowercase,
        k=random.randint(5, 10)
    ))
    username = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(5, 10)
    ))
    email = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(5, 10)
    )) + '@test.com'
    email2 = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(5, 10)
    )) + '@test.com'
    password = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=random.randint(5, 10)
    ))


    def test_incomplete_payload(self):
        firstname_only = requests.post(
            url=self.url,
            data=json.dumps({ 'firstname':  self.firstname }),
            headers=self.headers
        )
        lastname_only = requests.post(
            url=self.url,
            data=json.dumps({ 'lastname': self.lastname }),
            headers=self.headers
        )
        username_only = requests.post(
            url=self.url,
            data=json.dumps({ 'username': self.username }),
            headers=self.headers
        )
        email_only = requests.post(
            url=self.url,
            data=json.dumps({ 'email': self.email }),
            headers=self.headers
        )
        password_only = requests.post(
            url=self.url,
            data=json.dumps({ 'password': self.password }),
            headers=self.headers
        )

        self.assertEqual(firstname_only.status_code, 400)
        self.assertFalse(firstname_only.json()['status'])
        self.assertEqual(lastname_only.status_code, 400)
        self.assertFalse(lastname_only.json()['status'])
        self.assertEqual(username_only.status_code, 400)
        self.assertFalse(username_only.json()['status'])
        self.assertEqual(email_only.status_code, 400)
        self.assertFalse(email_only.json()['status'])
        self.assertEqual(password_only.status_code, 400)
        self.assertFalse(password_only.json()['status'])


    def test_on_success(self):
        payload = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        req = requests.post(
            url=self.url,
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(req.status_code, 201)
        self.assertTrue(req.json()['status'])
        self.assertIsNotNone(req.json()['access-token'])
        self.assertIsNotNone(req.json()['user-id'])
        self.assertIsInstance(req.json()['access-token'], str)
        self.assertIsNotNone(req.json()['message'])
        helpers.delete_user(req.json()['user-id'])


    def test_duplicate_credentials(self):
        # Get the credentials of an existing user
        existing_user = helpers.return_db_user()
        payload =  {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': existing_user['username'],
            'email': existing_user['email'],
            'password': self.password
        }

        payload['email'] = existing_user['email']
        duplicate_email = requests.post(
            url=self.url,
            data=json.dumps(payload),
            headers=self.headers
        )
        payload['username'] = existing_user['username']
        payload['email'] = self.email2
        duplicate_username = requests.post(
            url=self.url,
            data=json.dumps(payload),
            headers=self.headers
        )

        self.assertEqual(duplicate_username.status_code, 409)
        self.assertEqual(
            duplicate_username.json()['message'],
            'Failed to create user: username is taken'
        )
        self.assertFalse(duplicate_username.json()['status'])
        self.assertEqual(duplicate_email.status_code, 409)
        self.assertEqual(
            duplicate_email.json()['message'],
            'Failed to create user: email is taken'
        )
        self.assertFalse(duplicate_email.json()['status'])
        helpers.delete_user(existing_user['_id'])
