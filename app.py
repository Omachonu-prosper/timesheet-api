from flask import Flask, request, jsonify
from user_model import users

app = Flask(__name__)


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


@app.route('/')
def index():
	return "Timesheet API V-0.0.1", 200

if __name__ == '__main__':
	app.run(debug=True)