from app_logic.connect_to_db import db_utilities

def generate_employee_id():
    """
    Generate employee IDs for employees
        - Get the last id from the id counter
        - Generate a new id
        - Incriment the id counter
    """
    db_utils = db_utilities.find_one({}, {'id_counter': 1, '_id': 0})
    if not db_utils:
        # First employee record
        last_id = 0
    else:
        last_id = db_utils['id_counter']

    employee_id = f'IDL-{1 + last_id:06d}'
    db_utils = db_utilities.update_one(
        {}, {'$inc': {'id_counter': 1}}, upsert=True
    )
    return employee_id