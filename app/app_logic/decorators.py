import os
from flask import request, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from .connect_to_db import admins
from bson import ObjectId


# Decorator to make sure all endpoints cant be accessed without an api key
def api_key_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		server_api_key = os.environ.get('API_KEY', None)
		client_api_key = request.headers.get('x-api-key', None)
		if not client_api_key:
			return jsonify(
				{
					'message': 'Unauthorized: no API key was sent with the request header',
					'status': False
				}
			), 400
		if server_api_key != client_api_key:
			return jsonify(
				{
					'message': 'Unauthorized: invalid API key',
					'status': False
				}
			), 401
		return f(*args, **kwargs)
	return wrapper

# Decorator to protect admin only routes
def admin_protected(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		admin_identity = get_jwt_identity()
		admin = admins.find_one(
			{"_id": ObjectId(admin_identity)}
		)
		if admin is None:
			return jsonify({
				'message': 'Request Failed: you are not authorised to access this endpoint',
				'status': False
			}), 401
		
		return f(*args, **kwargs)
	return wrapper