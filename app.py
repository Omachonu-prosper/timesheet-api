from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from user_model import users

app = Flask(__name__)


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
	data = []
	for user in users:
		data.append(user['reports'])
	response = {
		"message": "Fetched report data successfully",
		"status": True,
		"data": data
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
		if today.weekday() == 0 and now.hour <= 8 and week_start == current_week - timedelta(weeks=1):
			pass
		else:
			return "Failed to record report: submission window exceeded", 403

	payload = {
		"id": 2,
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

	for user in users:
		if user['id'] == int(user_id):
			for report in user['reports']:
				if report['date'] == date:
					return 'Failed to record report: report already recorded', 403
			
			user['reports'].append(payload)
			response = {
				"message": "Report recorded successfully",
				"status": True,
				"data": None
			}
			return jsonify(response), 201
			
	return 'Failed to record report: user id not found', 404


@app.route('/')
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	app.run(debug=True)