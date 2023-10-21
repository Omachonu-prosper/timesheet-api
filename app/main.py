import os
import requests

from flask import jsonify, Blueprint
from app_logic.decorators import api_key_required
from dotenv import load_dotenv
from datetime import datetime

from app_logic.connect_to_db import api_statuses

load_dotenv()
main = Blueprint('main', __name__)


@main.route('/', strict_slashes=False)
@api_key_required
def index():
	return jsonify({
		'message': 'Timesheet API © IDL',
		'status': True
    }), 200


@main.route('/api/status', strict_slashes=False)
@api_key_required
def status():
	exec_start = datetime.now()
	BASE_URL = os.getenv('BASE_URL', None)
	API_KEY = os.getenv('API_KEY', None)
	if BASE_URL is None or API_KEY is None:
		return jsonify({
			'message': 'Insufficient config provided in environment: API status can not be verified',
			'status': False
		}), 206
	
	headers = {
		'x-api-key': API_KEY
	}
	
	# In these tests we are only interested that the status codes are not server related
	# (ie 5xx http status codes) so we do not worry about passing data to these endpoints
	view_all_reports = requests.get(url=f'{BASE_URL}/view/reports/all', headers=headers).status_code
	view_user_report = requests.get(url=f'{BASE_URL}/view/reports/6525926424f36006662d425f', headers=headers).status_code
	record_report_post = requests.post(url=f'{BASE_URL}/record/report', headers=headers).status_code
	record_report_put = requests.put(url=f'{BASE_URL}/record/report', headers=headers).status_code
	admin_login = requests.put(url=f'{BASE_URL}/admin/login', headers=headers).status_code
	user_login = requests.post(url=f'{BASE_URL}/user/login', headers=headers).status_code
	user_signup = requests.post(url=f'{BASE_URL}/user/signup', headers=headers).status_code
	user_account_info = requests.post(url=f'{BASE_URL}/user/account/personal-information', headers=headers).status_code
	index = requests.get(url=BASE_URL, headers=headers).status_code
	exec_end = datetime.now()
	exec_duration = exec_end - exec_start

	results = {
		'baseurl': BASE_URL,
		'execution_start': exec_start,
		'execution_end': exec_end,
		'execution_duration': f'{exec_duration.seconds} seconds, {exec_duration.microseconds} microseconds',
		'statuses': [
			{ 'endpoint': 'GET - /view/reports/all', 'status_code': view_all_reports },
			{ 'endpoint': 'GET - /view/reports/<user-id>', 'status_code': view_user_report },
			{ 'endpoint': 'POST - /record/report', 'status_code': record_report_post },
			{ 'endpoint': 'PUT - /record/report', 'status_code': record_report_put },
			{ 'endpoint': 'POST - /admin/login', 'status_code': admin_login },
			{ 'endpoint': 'POST - /user/login', 'status_code': user_login },
			{ 'endpoint': 'POST - /user/signup', 'status_code': user_signup },
			{ 'endpoint': 'GET - /', 'status_code': index },
			{ 'endpoint': 'POST - /user/signup', 'status_code': user_account_info }
		]
	}

	if view_all_reports > 499 or view_user_report > 499 or index > 499\
		or record_report_post > 499 or record_report_put > 499 or admin_login > 499\
		or user_login > 499 or user_signup > 499:
		remark = 'Internal server error detected: check database logs and admin mail for more info'
		results['remark'] = remark
		api_statuses.insert_one(results)
		return jsonify({
			'message': remark,
			'status': False
		}), 500
	
	remark = 'API is healthy and running'
	results['remark'] = remark
	api_statuses.insert_one(results)	
	return jsonify({
		'message': remark,
		'status': True
    }), 200
