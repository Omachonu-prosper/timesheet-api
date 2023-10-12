import os
from pymongo import MongoClient

# Pymongo instantiation
app_environment = os.environ.get('APP_ENVIRONMENT', 'development')
if app_environment.lower() == 'production':
	db_uri = os.environ.get('DB_URI')
else:
	db_uri = 'mongodb://localhost:27017/'

client = MongoClient(db_uri)
db = client['worksheet']
users = db['users']
admins = db['admins']
db_utilities = db['utilities']