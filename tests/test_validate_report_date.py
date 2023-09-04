import unittest

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
        validate_date2 = validate_report_date(date)

        self.assertEqual(validate_date['message'], 'Failed to record report: submission window exceeded')
        self.assertEqual(validate_date['error-code'], 403)
        self.assertTrue(validate_date['error'])
        self.assertEqual(validate_date2['message'], 'Failed to record report: submission window exceeded')
        self.assertEqual(validate_date2['error-code'], 403)
        self.assertTrue(validate_date2['error'])