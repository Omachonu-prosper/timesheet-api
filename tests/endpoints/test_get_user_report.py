import unittest
import helpers
import json
import requests
from datetime import datetime, timedelta

class TestGetUserReport(unittest.TestCase):
    """
    Test class for /view/reports/<string:user_id>

    Test Cases
    - Wrong access_token
    - No user or admin logged in
    - wrong user id
    - Admin access
    - User access
    - Without current-week query parameter
    - Wrong current-wek date format
    - With current-week query parameter
    """
    url = 'http://127.0.0.1:5000/view/reports/' # the userid is to be appended at the time of the request
    access_token = None
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json'
    }
    
    def setUp(self):
        # Login as an admin so dependent test cases can function properly
        admin_req = requests.post(
            url='http://127.0.0.1:5000/admin/login',
            headers=self.headers,
            data=json.dumps({
                'username': helpers.ADMIN_USERNAME,
                'password': helpers.ADMIN_PASSWORD
            })
        )
        self.admin_token = f"{admin_req.json()['access_token']}"

        # Login as a user so dependent test cases can function properly
        user = helpers.return_db_user()
        user_req = requests.post(
            url='http://127.0.0.1:5000/user/login',
            headers=self.headers,
            data=json.dumps({
                'email': user['email'],
                'password': user['password']
            })
        )
        self.user_token = f"{user_req.json()['access_token']}"
        self.user_id = user['_id']


    def test_wrong_access_token(self):
        helpers.delete_user(self.user_id)
        pass

    def test_no_user_or_admin(self):
        helpers.delete_user(self.user_id)
        pass

    def test_wrong_user_id(self):
        helpers.delete_user(self.user_id)
        pass

    def test_admin_access(self):
        helpers.delete_user(self.user_id)
        pass

    def test_user_access(self):
        helpers.delete_user(self.user_id)
        pass

    def test_with_curernt_week(self):
        helpers.delete_user(self.user_id)
        pass

    def test_wrong_current_week_format(self):
        helpers.delete_user(self.user_id)
        pass        

    def test_without_current_week(self):
        now = datetime.now()
        current_week = now - timedelta(days=now.weekday())
        week = current_week.strftime('%Y-%m-%d')

        # Test as an admin
        self.headers['Authorization'] = f"Bearer {self.admin_token}"
        req1 = requests.get(
            url=self.url + f"{self.user_id}",
            headers=self.headers
        )
        self.assertEqual(req1.status_code, 200)
        self.assertTrue(req1.json()['status'])
        self.assertIsInstance(req1.json()['data'], dict)
        self.assertEqual(req1.json()['week'], week)
        self.assertEqual(
            req1.json()['message'],
            'Fetched report data successfully'
        )

        # Test as a user
        self.headers['Authorization'] = f"Bearer {self.user_token}"
        req2 = requests.get(
            url=self.url + f"{self.user_id}",
            headers=self.headers
        )
        self.assertEqual(req2.status_code, 200)
        self.assertTrue(req2.json()['status'])
        self.assertIsInstance(req2.json()['data'], dict)
        self.assertEqual(req2.json()['week'], week)
        self.assertEqual(
            req2.json()['message'],
            'Fetched report data successfully'
        )
        helpers.delete_user(self.user_id)
