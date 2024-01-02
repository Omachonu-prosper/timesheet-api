"""
System related routes (CRUD operations for the system operations)
"""

from flask import request, jsonify
from bson import ObjectId
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required

# App logic dependencies
from core import app
from core.utils.connect_to_db import users
from core.utils.validate_record_report import validate_record_report
from core.utils.validate_report_date import validate_report_date
from core.utils.format_data import format_data
from core.utils.decorators import api_key_required, admin_protected


@app.route('/view/reports/all', strict_slashes=False)
@api_key_required
@jwt_required()
@admin_protected
def get_all_reports():
	# If there is no current-week query parameter make the system use the previous week
	current_week = request.args.get('current-week', None)
	if current_week:
		try:
			current_week = datetime.strptime(current_week, '%Y-%m-%d').strftime('%Y-%m-%d')
		except:
			return jsonify({
				'message': 'Failed to fetch report data: current_week is not a valid date format',
				'status': False
			}), 400
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


@app.route('/view/reports/<string:user_id>', strict_slashes=False)
@api_key_required
@jwt_required()
def get_user_reports(user_id):
	# If there is no current-week query parameter make the system use the current week
	current_week = request.args.get('current-week', None)
	if current_week:
		try:
			current_week = datetime.strptime(current_week, '%Y-%m-%d').strftime('%Y-%m-%d')
		except:
			return jsonify({
				'message': 'Failed to fetch report data: current_week is not a valid date format',
				'status': False
			}), 400
	else:
		now = datetime.now()
		current_week = now - timedelta(days=now.weekday())
		current_week = current_week.strftime('%Y-%m-%d')

	# Fetch all reports for a specific user for the current week
	try:
		_id = ObjectId(user_id)
	except:
		return jsonify({
			'message': 'Failed to fetch reports: invalid user id',
			'status': False
		}), 422

	data = users.find(
		{"_id": _id},
		{
			f"reports.{current_week}": 1,
			"username": 1,
			"email": 1
		}
	)
	data = list(data)
	if not data:
		return jsonify({
			'message': 'Failed to fetch reports: user id not found',
			'status': False
		}), 404
	
	# Since formated_data returns an array of objects we get the first (and only)
	# object from the returned data and send that to the client
	formated_data = format_data(data, current_week)[0]

	response = {
		"message": "Fetched report data successfully",
		"week": current_week,
		"status": True,
		"data": formated_data
	}
	return jsonify(response), 200


@app.route('/record/report', methods=['POST', 'PUT'], strict_slashes=False)
@api_key_required
@jwt_required()
def record_report():
	response = validate_record_report(request.json)
	if response.get('error'):
		return jsonify({
			'message': response['message'],
			'status': False
		}), response['error-code']

	dates = validate_report_date(response['date'])
	if dates.get('error'):
		return jsonify({
			'message': dates['message'],
			'status': False
		}), dates['error-code']

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
			return jsonify({
				'message': 'Failed to record report: report already recorded',
				'status': False
			}), 409

		status_code = 201
		status_message = "Report recorded successfully"
		failure_message = "Failed to record report: User ID not found"
	
	elif request.method == 'PUT':
		if  not len(list(report_exists)):
			return jsonify({
				'message': 'Failed to update report: report not found',
				'status': False
			}), 404
		
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
		return jsonify({
			'message': failure_message,
			'status': False
		}), 404
		
	response = {
		"message": status_message,
		"status": True,
		"data": None
	}
	return jsonify(response), status_code
