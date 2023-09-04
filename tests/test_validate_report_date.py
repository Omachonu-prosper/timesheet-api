import unittest

from datetime import datetime
from app_logic.validate_report_date import validate_report_date

"""
Unittest for the function that validates a date,
and checks if a date is within the current submission window

# Test cases
- valid dates (outside the submission window)
- valid dates (within the submission window)
- Invalid dates
"""

class TestValidateReportDate(unittest.TestCase):
    def test_valid_outside_sub_window(self):
        date = '2023-08-01'
        date2 = '2025-08-01'
        validate_date = validate_report_date(date)
        validate_date2 = validate_report_date(date2)

        self.assertEqual(validate_date['message'], 'Failed to record report: submission window exceeded')
        self.assertEqual(validate_date['error-code'], 403)
        self.assertTrue(validate_date['error'])
        self.assertEqual(validate_date2['message'], 'Failed to record report: submission window exceeded')
        self.assertEqual(validate_date2['error-code'], 403)
        self.assertTrue(validate_date2['error'])

    def test_valid_within_sub_window(self):
        date = datetime.now().strftime('%Y-%m-%d')
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        validate_date = validate_report_date(date)

        self.assertIsNone(validate_date.get('error'))
        self.assertEqual(validate_date['date'], date_obj)
        self.assertIsNotNone(validate_date['day'])
        self.assertIsNotNone(validate_date['week'])
        self.assertIsNotNone(validate_date['created-at'])

    def test_invalid_date(self):
        date = '2023-45-90'
        date2 = '04-05-2023'
        date3 = 'not-a-date'
        validate_date = validate_report_date(date)
        validate_date2 = validate_report_date(date2)
        validate_date3 = validate_report_date(date3)

        self.assertEqual(validate_date['message'], 'Date is not a valid datetime format')
        self.assertEqual(validate_date['error-code'], 400)
        self.assertTrue(validate_date['error'])
        self.assertEqual(validate_date2['message'], 'Date is not a valid datetime format')
        self.assertEqual(validate_date2['error-code'], 400)
        self.assertTrue(validate_date2['error'])
        self.assertEqual(validate_date3['message'], 'Date is not a valid datetime format')
        self.assertEqual(validate_date3['error-code'], 400)
        self.assertTrue(validate_date3['error'])