import os

from dotenv import load_dotenv
from bson import ObjectId
from app_logic.connect_to_db import users

load_dotenv()
API_KEY = os.environ.get('API_KEY', None)

# Create a helper to create users (signup)
def create_user(username=None, email=None, password=None):
    pass

# Create a helper to test for api-keys and access-tokens for endpoints
def api_key_required():
    pass

# Delete users from db after creation
def delete_user(user_id):
    user = users.delete_one({"_id": ObjectId(user_id)})
    if user.deleted_count != 1:
        return False
    return True