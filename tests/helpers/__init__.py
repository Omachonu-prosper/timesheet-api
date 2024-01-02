import os

from flask_bcrypt import generate_password_hash
from dotenv import load_dotenv
from bson import ObjectId
from core.utils.connect_to_db import users, db_utilities

load_dotenv()
API_KEY = os.environ.get('API_KEY', None)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', None)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', None)

# Returns a user object from the database which can be used in test cases
def return_db_user():
    user_obj = {
        'username': 'Test-user',
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'testuser@example.com',
        'password': generate_password_hash('password')
    }
    user = users.insert_one(user_obj)
    if user.acknowledged:
        user_obj['_id'] = str(user.inserted_id)
        user_obj['password'] = 'password'
        return user_obj
    else:
        return False


# Delete users from db after creation
def delete_user(user_id):
    user = users.delete_one({"_id": ObjectId(user_id)})
    if user.deleted_count != 1:
        return False
    return True