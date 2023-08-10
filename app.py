from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson import ObjectId
from uuid import uuid1


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['worksheet']
col = db['users']


def get_day_of_week(date):
	weekday = date.weekday()

	match weekday:
		case 0:
			return "Monday"
		case 1:
			return "Tuesday"
		case 2:
			return "Wednesday"
		case 3:
			return "Thursday"
		case 4:
			return "Friday"
		case 5:
			return "Saturday"
		case 6:
			return "Sunday"


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


@app.route('/record/report/<string:user_id>', methods=['POST'])
def record_report(user_id):
	date = request.json.get('date')
	project = request.json.get('project')
	task = request.json.get('task')
	status = request.json.get('status')
	link = request.json.get('link')
	duration = request.json.get('duration')

	if not date or not project or not task or not status or not link or not duration:
		return 'Missing required parameter', 400

	try:
		date = datetime.strptime(date, "%Y-%m-%d")
		week_start = date - timedelta(days=date.weekday())
		created_at = datetime.now()
		day_of_week = get_day_of_week(date)
		
		now = datetime.now()
		today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
		current_week = today - timedelta(days=today.weekday())
	except:
		return 'Date is not a valid datetime format', 400


	if current_week != week_start:
		# Once it is past 8:00am on Monday do not accept submissions for any other week apart from the current week
		# today.weekday == 0 (shows that it is a monday)
		# now.hour < 8 (the time is not yet 8:00am)
		# week_start == current_week - timedelta(weeks=1) 
		# 	(shows that the report we are trying to submit is a report of the past week
		# 	and so can be allowed since the time is not yet 8:00am)
		if today.weekday() == 0 and now.hour < 8 and week_start == current_week - timedelta(weeks=1):
			pass
		else:
			return "Failed to record report: submission window exceeded", 403

	payload = {
		"id": str(uuid1()),
		"date": date,
		"project": project,
		"task": task,
		"link": link,
		"status": status,
		"duration": duration,
		"day-of-week": day_of_week,
		"week-start": week_start,
		"created-at": created_at
	}

	# return 'Failed to record report: report already recorded', 409
	report_exists = col.find({
		'_id': ObjectId(user_id),
		'reports.date': date
		}, {'_id': 1})
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

@app.route('/')
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	app.run(debug=True)