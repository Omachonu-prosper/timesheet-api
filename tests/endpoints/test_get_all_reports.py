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
    - Wrong current-wek date format
    - With current-week query parameter
    """
    url = 'http://127.0.0.1:5000/view/reports/all'
    access_token = None
    headers = {
        'x-api-key': helpers.API_KEY,
        'Content-Type': 'application/json'
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
        self.headers['Authorization'] = f"Bearer {req.json()['access_token']}"


    def test_wrong_access_token(self):
        self.headers['Authorization'] = "Wrong token"
        req = requests.get(
            url=self.url,
            headers=self.headers
        )
        self.assertEqual(req.status_code, 401)
        

    def test_not_admin(self):
        user = helpers.return_db_user()
        email = user['email']
        password = user['password']
        login_req =  requests.post(
            url='http://127.0.0.1:5000/user/login',
            headers=self.headers,
            data=json.dumps({
                'email': email,
                'password': password
            })
        )
        self.headers['Authorization'] = f"Bearer {login_req.json()['access_token']}"
        helpers.delete_user(user['_id'])
        
        req = requests.get(
            url=self.url,
            headers=self.headers
        )
        self.assertEqual(req.status_code, 401)
        self.assertFalse(req.json()['status'])
        self.assertEqual(
            req.json()['message'],
            'Request Failed: you are not authorised to access this endpoint'
        )


    def test_with_curernt_week(self):
        week = '2023-09-11'
        req = requests.get(
            url=self.url + f'?current-week={week}',
            headers=self.headers
        )
        self.assertEqual(req.status_code, 200)
        self.assertTrue(req.json()['status'])
        self.assertIsInstance(req.json()['data'], list)
        self.assertEqual(req.json()['week'], week)
        self.assertEqual(
            req.json()['message'],
            'Fetched report data successfully'
        )
        

    def test_wrong_current_week_format(self):
        week1 = 'not-a-week'
        week2 = '20-20-2020'
        req1 = requests.get(
            url=self.url + f'?current-week={week1}',
            headers=self.headers
        )
        self.assertEqual(req1.status_code, 400)
        self.assertFalse(req1.json()['status'])
        self.assertEqual(
            req1.json()['message'],
            'Failed to fetch report data: current_week is not a valid date format'
        )

        req2 = requests.get(
            url=self.url + f'?current-week={week2}',
            headers=self.headers
        )
        self.assertEqual(req2.status_code, 400)
        self.assertFalse(req2.json()['status'])
        self.assertEqual(
            req2.json()['message'],
            'Failed to fetch report data: current_week is not a valid date format'
        )
        

    def test_without_current_week(self):
        pass
