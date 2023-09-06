import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY', None)

# Create a helper to create users (signup)
# Create a helper to test for api-keys and access-tokens or endpoints
# Delete users from db after creation