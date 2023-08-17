# External libraries and dependencies
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# App logic dependencies
from app_logic.validate_record_report import validate_record_report
from app_logic.validate_report_date import validate_report_date
from app_logic.validate_signup_data import validate_signup_data
from app_logic.format_data import format_data
from app_logic.decorators import api_key_required


# Load all environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'SECRET')

# Bcrypt instantiation
bcrypt = Bcrypt(app)

# JWT instantiation 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(weeks=1)
jwt = JWTManager(app)

# Pymongo instantiation
app_environment = os.environ.get('APP_ENVIRONMENT', 'development')
if app_environment.lower() == 'production':
	db_uri = os.environ.get('DB_URI')
else:
	db_uri = 'mongodb://localhost:27017/'

client = MongoClient(db_uri)
db = client['worksheet']
users = db['users']
	

@app.route('/user/login', methods=['POST'])
@api_key_required
def login():
	data = request.json
	email = data.get('email', None)
	password = data.get('password', None)
	if not email or not password:
		return 'Missing required parameter', 400

	user = users.find_one(
		{'email': email},
		{'_id': 1, 'password': 1}
	)
	if user is None:
		return "Failed to log user in: email not found", 404
	password_matchs = bcrypt.check_password_hash(user['password'], password)
	if not password_matchs:
		return "Failed to log user in: invalid credentials", 404
		
	user_id = str(user['_id'])
	token = create_access_token(identity=user_id)
	response = {
		'access_token': token,
		'message': 'Login successful',
		'user-id': user_id,
		'data': None,
		'status': True
	}
	return jsonify(response)


@app.route('/user/signup', methods=['POST'])
@api_key_required
def signup():
	validate_signup = validate_signup_data(request.json)
	if validate_signup.get('error'):
		return validate_signup['message'], validate_signup['error-code']

	# Check if a user with the email already exists
	user = users.find_one(
		{"email": validate_signup['email']},
		{"_id": 1}
	)
	if user is not None:
		return "Failed to create user: email is taken", 409
	
	# Check if a user with the username already exists
	user = users.find_one(
		{"username": validate_signup['username']},
		{"_id": 1}
	)
	if user is not None:
		return "Failed to create user: username is taken", 409
	
	validate_signup['password'] = bcrypt.generate_password_hash(validate_signup['password'])
	insert = users.insert_one(validate_signup)
	user_id = str(insert.inserted_id)
	if not insert.acknowledged:
		return "Failed to create user: an error occured", 500
	
	token = create_access_token(identity=user_id)
	response = {
		'message': "User created successfully",
		'data': None,
		'access-token': token,
		'user-id': user_id,
		'status': True
	}
	return response, 201


@app.route('/view/reports/all')
@api_key_required
def get_all_reports():
	# If there is no current-week query parameter make the system use the previous week
	current_week = request.args.get('current-week', None)
	if current_week:
		try:
			current_week = datetime.strptime(current_week, '%Y-%m-%d').strftime('%Y-%m-%d')
		except:
			return "Failed to fetch report data: current_week is not a valid date format", 400
	else:
		now = datetime.now()
		current_week = now - timedelta(days=now.weekday(), weeks=1)
		current_week = current_week.strftime('%Y-%m-%d')

	# Fetch all reports for each user for the current week
	data = users.find({}, {
		f"reports.{current_week}": 1,
		"username": 1,
		"lastname": 1,
		"middlename": 1,
		"firstname": 1,
		"email": 1
	})
	formated_data = format_data(data, current_week)

	response = {
		"message": "Fetched report data successfully",
		"week": current_week,
		"status": True,
		"data": formated_data
	}
	return jsonify(response)


@app.route('/view/reports/<string:user_id>')
@api_key_required
def get_user_reports(user_id):
	# If there is no current-week query parameter make the system use the current week
	current_week = request.args.get('current-week', None)
	if current_week:
		try:
			current_week = datetime.strptime(current_week, '%Y-%m-%d').strftime('%Y-%m-%d')
		except:
			return "Failed to fetch report data: current_week is not a valid date format", 400
	else:
		now = datetime.now()
		current_week = now - timedelta(days=now.weekday())
		current_week = current_week.strftime('%Y-%m-%d')

	# Fetch all reports for a specific user for the current week
	data = users.find(
		{"_id": ObjectId(user_id)},
		{
			f"reports.{current_week}": 1,
			"username": 1,
			"email": 1
		}
	)
	data = list(data)
	if not data:
		return "Failed to fetch reports: user id not found", 404
	
	# Since formated_data returns an array of objects we get the first (and only)
	# object from the returned data and send that to the user
	formated_data = format_data(data, current_week)[0]

	response = {
		"message": "Fetched report data successfully",
		"week": current_week,
		"status": True,
		"data": formated_data
	}
	return jsonify(response)


@app.route('/record/report', methods=['POST', 'PUT'])
@api_key_required
@jwt_required()
def record_report():
	response = validate_record_report(request.json)
	if response.get('error'):
		return response['message'], response['error-code']

	dates = validate_report_date(response['date'])
	if dates.get('error'):
		return dates['message'], dates['error-code']

	user_id = get_jwt_identity()
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

	# Check if a report has been recorded
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
@api_key_required
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	if app_environment.lower() == 'production':
		app.run()
	else:
		app.run(debug=True)