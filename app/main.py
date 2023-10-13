from flask import jsonify, Blueprint
from app_logic.decorators import api_key_required

main = Blueprint('main', __name__)


@main.route('/', strict_slashes=False)
@api_key_required
def index():
	return jsonify({
		'message': 'Timesheet API © IDL',
		'status': True
    }), 200


@main.route('/api/status')
@api_key_required
def status():
	return jsonify({
		'message': 'API is healthy and running',
		'status': True
    }), 200
