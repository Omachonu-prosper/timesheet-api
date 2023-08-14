from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId
from functools import wraps

import jwt

from app_logic.validate_record_report import validate_record_report
from app_logic.validate_report_date import validate_report_date
from app_logic.validate_signup_data import validate_signup_data
from app_logic.format_data import format_data


app = Flask(__name__)
SECRET_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoieydfaWQnOiBPYmplY3RJZCgnNjRkOTIzMDc3MWUwNDVhN2Y5NzkxMWU1Jyl9IiwiZXhwIjoxNjkyMDI1NDM1fQ.x8raWx4SQMW_uD5XA-SV1GazIpcxDc3JmvXhyR-KWUA'
algorithm = 'HS256'
client = MongoClient("mongodb://localhost:27017/")
db = client['worksheet']
users = db['users']


def generate_jwt(user_id, remember_me):
	if remember_me:
		expiry = datetime.utcnow() + timedelta(weeks=1)
	else:
		expiry = datetime.utcnow() + timedelta(hours=1)
	payload = {
		'user_id': str(user_id),
		'exp': expiry
	}
	token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
	return token

def verify_jwt(token):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=algorithm)
		return payload
	except jwt.ExpiredSignatureError:
		return {
			'error': True,
			'message': 'Session expired: login required',
			'error-code': 401
		}
	except jwt.InvalidTokenError:
		return {
			'error': True,
			'message': 'Invalid token: bad request header',
			'error-code': 400
		}


def jwt_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		token = request.headers.get('Authorization')
		if not token:
			return "Failed to access endpoint: access token not provided", 401

		token = token.split()[1]
		payload = verify_jwt(token)
		if payload.get('error'):
			return payload['message'], payload['error-code']
		
		return func(*args, **kwargs)
	return wrapper


@app.route('/user/login', methods=['POST'])
def login():
	data = request.json
	remember_me = data.get('remember-me')
	username = data.get('username')
	password = data.get('password')

	user = users.find(
		{'username': username, 'password': password},
		{'_id': 1}
	)
	user = list(user)
	if not user:
		return "Failed to authenticate user: Invalid credentials", 401
	
	user_id = user[0]
	token = generate_jwt(user_id, remember_me)
	return jsonify({'access_token': token}), 200


@app.route('/user/signup', methods=['POST'])
def signup():
	validate_signup = validate_signup_data(request.json)
	if validate_signup.get('error'):
		return validate_signup['message'], validate_signup['error-code']

	# Check if a user with the username already exists
	user = users.find(
		{"username": validate_signup['username']},
		{"_id": 1}
	)
	if list(user):
		return "Failed to create user: username is taken", 409
	
	insert = users.insert_one(validate_signup)
	if not insert.acknowledged:
		return "Failed to create user: an error occured", 500
	
	response = {
		'message': "User created successfully",
		'data': None,
		'status': True
	}
	return response, 201



@app.route('/view/reports/all')
def get_all_reports():
	now = datetime.now()
	current_week = now - timedelta(days=now.weekday(), weeks=1)
	current_week = current_week.strftime('%Y-%m-%d')

	# Fetch all reports for each user for the current week
	data = users.find({}, {"_id": 0, f"reports.{current_week}": 1, "username": 1})
	formated_data = format_data(data, current_week)
	
	response = {
		"message": "Fetched report data successfully",
		"week": current_week,
		"status": True,
		"data": formated_data
	}
	return jsonify(response)


@app.route('/view/reports/<string:user_id>')
@jwt_required
def get_user_reports(user_id):
	now = datetime.now()
	current_week = now - timedelta(days=now.weekday())
	current_week = current_week.strftime('%Y-%m-%d')

	# Fetch all reports for a specific user for the current week
	data = users.find(
		{"_id": ObjectId(user_id)},
		{"_id": 0, f"reports.{current_week}": 1, "username": 1}
	)
	data = list(data)
	if not data:
		return "Failed to fetch reports: user id not found", 404
	formated_data = format_data(data, current_week)

	response = {
		"message": "Fetched report data successfully",
		"week": current_week,
		"status": True,
		"data": formated_data
	}
	return jsonify(response)


@app.route('/record/report/<string:user_id>', methods=['POST', 'PUT'])
def record_report(user_id):
	response = validate_record_report(request.json)
	if response.get('error'):
		return response['message'], response['error-code']

	dates = validate_report_date(response['date'])
	if dates.get('error'):
		return dates['message'], dates['error-code']

	payload = {
		"date": dates['date'],
		"project": response['project'],
		"task": response['task'],
		"link": response['link'],
		"status": response['status'],
		"duration": response['duration'],
		"day-of-week": dates['day'],
		"modified-at": dates['created-at']
	}

	# Check if a recport has been recorded
	report_exists = users.find(
		{
			'_id': ObjectId(user_id),
			f"reports.{dates['week']}.{dates['day'].lower()}.day-of-week": dates['day']
		},
		{'_id': 1}
	)
	
	if request.method == 'POST':
		if len(list(report_exists)):
			return 'Failed to record report: report already recorded', 409

		status_code = 201
		status_message = "Report recorded successfully"
		failure_message = "Failed to record report: User ID not found"
	
	elif request.method == 'PUT':
		if  not len(list(report_exists)):
			return 'Failed to update report: report not found', 404
		
		status_code = 200
		status_message = "Report updated successfully"
		failure_message = "Failed to update report: User ID not found"
		
	insert = users.update_one(
		{'_id': ObjectId(user_id)},
		{"$set": {
			f"reports.{dates['week']}.{dates['day'].lower()}": payload
		}}
	)
	if insert.matched_count != 1:
		return failure_message, 404
		
	response = {
		"message": status_message,
		"status": True,
		"data": None
	}
	return jsonify(response), status_code


@app.route('/')
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	app.run(debug=True)