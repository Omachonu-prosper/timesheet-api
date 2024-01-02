import unittest

from datetime import datetime
from core.utils.get_day_of_week import get_day_of_week


"""
Test the function that gets the day of the week from a given date

- To be tested with known dates and their days of the week
- Date strings are in the format YYYY-MM-DD

# Test cases
    - valid dates
"""
class TestGetDayOfWeek(unittest.TestCase):
    def test_valid_dates(self):
        day1 = datetime.strptime('2023-09-01', '%Y-%m-%d')
        day2 = datetime.strptime('2023-09-02', '%Y-%m-%d')
        day3 = datetime.strptime('2023-09-03', '%Y-%m-%d')
        day4 = datetime.strptime('2023-09-04', '%Y-%m-%d')
        day5 = datetime.strptime('2023-09-05', '%Y-%m-%d')
        day6 = datetime.strptime('2023-09-06', '%Y-%m-%d')
        day7 = datetime.strptime('2023-09-07', '%Y-%m-%d')

        day_of_week1 = get_day_of_week(day1)
        day_of_week2 = get_day_of_week(day2)
        day_of_week3 = get_day_of_week(day3)
        day_of_week4 = get_day_of_week(day4)
        day_of_week5 = get_day_of_week(day5)
        day_of_week6 = get_day_of_week(day6)
        day_of_week7 = get_day_of_week(day7)

        self.assertEqual(day_of_week1, 'Friday')
        self.assertEqual(day_of_week2, 'Saturday')
        self.assertEqual(day_of_week3, 'Sunday')
        self.assertEqual(day_of_week4, 'Monday')
        self.assertEqual(day_of_week5, 'Tuesday')
        self.assertEqual(day_of_week6, 'Wednesday')
        self.assertEqual(day_of_week7, 'Thursday')
