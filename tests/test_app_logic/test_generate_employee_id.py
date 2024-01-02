import unittest

from tests.helpers import db_utilities
from core.utils.generate_employee_id import generate_employee_id


"""
Test function that generates employee IDs for employees

Test cases
- Correct id is generated
- Id counter is incrimented
"""
class TestGenerateEmployeeId(unittest.TestCase):    
    def test_correct_id_generated(self):
        db_utils = db_utilities.find_one({}, {'id_counter': 1, '_id': 0})
        last_id = db_utils['id_counter']

        expected_id = f'IDL-{1 + last_id:06d}'
        generated_id = generate_employee_id()
        self.assertEqual(expected_id, generated_id)

    
    def test_counter_is_incrimented(self):
        db_utils = db_utilities.find_one({}, {'id_counter': 1, '_id': 0})
        last_id = db_utils['id_counter']
        generate_employee_id()
        db_utils = db_utilities.find_one({}, {'id_counter': 1, '_id': 0})
        new_id = db_utils['id_counter']
        self.assertEqual(last_id + 1, new_id)