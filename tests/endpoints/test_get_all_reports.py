import unittest
import json
import requests
import helpers

class TestGetAllReports(unittest.TestCase):
    """
    Test class to test /view/reports/all

    Test Cases
    - Try it without an admin login
    - Wrong access_token
    - Without current-week query parameter
    - With current-week query parameter
    """
    url = 'http://127.0.0.1:5000/view/reports/all'
    access_token = None
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    def setUp(self):
        # Login as an admin so other testcases can function properly
        req = requests.post(
            url='http://127.0.0.1:5000/admin/login',
            headers=self.headers,
            data=json.dumps({
                'username': helpers.ADMIN_USERNAME,
                'password': helpers.ADMIN_PASSWORD
            })
        )
        self.access_token = req.json()['access_token']


    def test_wrong_access_token(self):
        self.access_token = 'Wrong token'
        req = requests.get(
            url=self.url,
            headers=self.headers
        )
        self.assertEqual(req.status_code, 422)
        

    def test_not_admin(self):
        pass

    def test_with_curernt_week(self):
        pass

    def test_without_current_week(self):
        pass

