import os
from flask import request
from functools import wraps


# Decorator to make sure all endpoints cant be accessed without an api key
def api_key_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		server_api_key = os.environ.get('API_KEY', None)
		client_api_key = request.headers.get('x-api-key', None)
		if not client_api_key:
			return "Unauthorized: no API key was sent with the request header", 400
		if server_api_key != client_api_key:
			return "Unauthorized: invalid API key", 401
		return f(*args, **kwargs)
	return wrapper