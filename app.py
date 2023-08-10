from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId
from uuid import uuid1

from app_logic.validate_record_report import validate_record_report
from app_logic.validate_report_date import validate_report_date


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['worksheet']
col = db['users']


@app.route('/view/reports/all')
def get_all_reports():
	now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
	current_week_start = now - timedelta(days=now.weekday())

	# Fetch all reports for each user for the current week sorted by date
	data = col.aggregate([
		{"$match": {"reports.week-start": current_week_start}},
		{"$sort": {"reports.date": 1}},
		{"$project": {"reports": 1, "_id": 0, "username": 1}}
	])
	response = {
		"message": "Fetched report data successfully",
		"status": True,
		"data": list(data)
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
	# Copies the values of dates to the response dictionary
	response.update(dates)

	payload = {
		"id": str(uuid1()),
		"date": response['date'],
		"project": response['project'],
		"task": response['task'],
		"link": response['link'],
		"status": response['status'],
		"duration": response['duration'],
		"day-of-week": response['day-of-week'],
		"week-start": response['week-start'],
		"created-at": response['created-at']
	}
		
	if request.method == 'POST':
		# Prevent duplicate report recording
		report_exists = col.find(
			{'_id': ObjectId(user_id), 'reports.date': response['date']},
			{'_id': 1}
		)
		if list(report_exists):
			return 'Failed to record report: report already recorded', 409

		insert = col.update_one({'_id': ObjectId(user_id)}, {'$push': {'reports': payload}})
		if not insert.matched_count:
			return 'Failed to record report: user id not found', 404

		response = {
			"message": "Report recorded successfully",
			"status": True,
			"data": None
		}
		return jsonify(response), 201
	
	elif request.method == 'PUT':
		update = col.update_one(
			{"_id": ObjectId(user_id), "reports.date": response['date']},
			{"$set": {
				"reports.$.link": payload['link'],
				"reports.$.project": payload['project'],
				"reports.$.status": payload['status'],
				"reports.$.duration": payload['task'],
				"reports.$.task": payload['task']
			}}
		)
		if update.matched_count != 1:
			return "Failed to update report: report was not found", 404
		
		response = {
			"message": "Report updated successfully",
			"status": True,
			"data": None
		}
		return jsonify(response), 200


@app.route('/')
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	app.run(debug=True)