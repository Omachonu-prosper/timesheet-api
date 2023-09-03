import unittest
import requests
import os
import json
import string
import random

from dotenv import load_dotenv

# Load all environment variables
load_dotenv()

class TestRoutes(unittest.TestCase):
    API_KEY = os.environ.get('API_KEY', None)
    
    def test_index(self):
        """
        Test function to test '/' route

        - On success a 200 status code is returned
        - If no API key is sent with the request a 400 error code is returned
        - If a wrong API key is sent a 401 UNAUTHORIZED error is returned
        """
        url = 'http://127.0.0.1:5000/'
        correct_headers = {
            'x-api-key': self.API_KEY
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
        
    def test_signup(self):
        """
        Test function to test /user/signup

        - All required payload must be sent else an appropriate error is returned
        - A user cant sign up with credentials that have been taken by other users
        - 201 CREATED status code is returned on success
        - The response JSON on success must have an access-token, a user-id and a status of True
        """
        url = 'http://127.0.0.1:5000/user/signup'
        headers = {
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/json'
        }

        # Generate random strings to be used as test data
        firstname = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        lastname = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))
        username2 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))
        email = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10))) + '@test.com'
        email2 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10))) + '@test.com'
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 10)))

        # Complete payload
        complete_payload = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'email': email,
            'password': password
        }

        # Testing incomplete payloads
        firstname_only = requests.post(url=url, data=json.dumps({ 'firstname':  firstname }), headers=headers)
        lastname_only = requests.post(url=url, data=json.dumps({ 'lastname': lastname }), headers=headers)
        username_only = requests.post(url=url, data=json.dumps({ 'username': username }), headers=headers)
        email_only = requests.post(url=url, data=json.dumps({ 'email': email }), headers=headers)
        password_only = requests.post(url=url, data=json.dumps({ 'password': password }), headers=headers)

        # Testing complete payload
        complete_payload_request = requests.post(url=url, data=json.dumps(complete_payload), headers=headers)

        # Testing duplicate user
        complete_payload['username'] = username2
        complete_payload['email'] = email
        duplicate_email = requests.post(url=url, data=json.dumps(complete_payload), headers=headers)
        complete_payload['username'] = username
        complete_payload['email'] = email2
        duplicate_username = requests.post(url=url, data=json.dumps(complete_payload), headers=headers)
        
        # Assert that all requests with incomplete payloads return 400 status codes
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

        # Assert that the request with complete payload returns a 201 created and returns correct data
        self.assertEqual(complete_payload_request.status_code, 201)
        self.assertTrue(complete_payload_request.json()['status'])
        self.assertIsNotNone(complete_payload_request.json()['access-token'])
        self.assertIsInstance(complete_payload_request.json()['access-token'], str)

        # Assert that duplicate user request returns an error
        self.assertEqual(duplicate_username.status_code, 409)
        self.assertEqual(duplicate_username.json()['message'], 'Failed to create user: username is taken')
        self.assertFalse(duplicate_username.json()['status'])
        self.assertEqual(duplicate_email.status_code, 409)
        self.assertEqual(duplicate_email.json()['message'], 'Failed to create user: email is taken')
        self.assertFalse(duplicate_email.json()['status'])

