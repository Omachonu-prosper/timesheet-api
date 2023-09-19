import unittest
import requests


"""
This module contains a series of tests, testing that all protected
endpoints can not be accessed without proper credentials

Test cases for TestAuthorization
- Send requests without API keys
- Send requests with wrong API keys
"""
class TestAuthorization(unittest.TestCase):    
    def make_request(self, url, method):
        headers = {
            'x-api-key': 'Wrong-Api-Key'
        }
    
        if method == 'GET':
            req_with_header = requests.get(url=url, headers=headers)
            req_without_header = requests.get(url=url)
        elif method == 'POST':
            req_with_header = requests.post(url=url, headers=headers)
            req_without_header = requests.post(url=url)
        elif method == 'PUT':
            req_with_header = requests.put(url=url, headers=headers)
            req_without_header = requests.put(url=url)
        else:
            return 'HTTP method not supported'
        

        self.assertEqual(req_with_header.status_code, 401)
        self.assertFalse(req_with_header.json()['status'])
        self.assertEqual(
            req_with_header.json()['message'],
            'Unauthorized: invalid API key'
        )
        self.assertEqual(req_without_header.status_code, 400)
        self.assertFalse(req_without_header.json()['status'])
        self.assertEqual(
            req_without_header.json()['message'],
            'Unauthorized: no API key was sent with the request header'
        )

    
    def test_index(self):
        self.make_request('http://127.0.0.1:5000/', 'GET')


    def test_login(self):
        self.make_request('http://127.0.0.1:5000/user/login', 'POST')


    def test_admin_login(self):
        self.make_request('http://127.0.0.1:5000/admin/login', 'POST')


    def test_signup(self):
        self.make_request('http://127.0.0.1:5000/user/signup', 'POST')


    def test_get_all_reports(self):
        self.make_request('http://127.0.0.1:5000/view/reports/all', 'GET')


    def test_get_user_reports(self):
        self.make_request('http://127.0.0.1:5000/view/reports/random-user-id', 'GET')


    def test_record_report_post(self):
        self.make_request('http://127.0.0.1:5000/record/report', 'POST')


    def test_record_report_put(self):
        self.make_request('http://127.0.0.1:5000/record/report', 'PUT')
