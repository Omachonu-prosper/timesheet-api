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
    username2 = ''.join(random.choices(
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
    complete_payload = {
        'firstname': firstname,
        'lastname': lastname,
        'username': username,
        'email': email,
        'password': password
    }


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
        req = requests.post(
            url=self.url,
            data=json.dumps(self.complete_payload),
            headers=self.headers
        )
        
        self.assertEqual(req.status_code, 201)
        self.assertTrue(req.json()['status'])
        self.assertIsNotNone(req.json()['access-token'])
        self.assertIsInstance(req.json()['access-token'], str)
        self.assertIsNotNone(req.json()['message'])


    # def test_duplicate_credentials(self):
    #     self.complete_payload['username'] = self.username2
    #     self.complete_payload['email'] = self.email
    #     duplicate_email = requests.post(
    #         url=self.url,
    #         data=json.dumps(self.complete_payload),
    #         headers=self.headers
    #     )
    #     self.complete_payload['username'] = self.username
    #     self.complete_payload['email'] = self.email2
    #     duplicate_username = requests.post(
    #         url=self.url,
    #         data=json.dumps(self.complete_payload),
    #         headers=self.headers
    #     )

    #     self.assertEqual(duplicate_username.status_code, 409)
    #     self.assertEqual(
    #         duplicate_username.json()['message'],
    #         'Failed to create user: username is taken'
    #     )
    #     self.assertFalse(duplicate_username.json()['status'])
    #     self.assertEqual(duplicate_email.status_code, 409)
    #     self.assertEqual(
    #         duplicate_email.json()['message'],
    #         'Failed to create user: email is taken'
    #     )
    #     self.assertFalse(duplicate_email.json()['status'])
