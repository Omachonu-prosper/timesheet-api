from flask import jsonify
from core import app


@app.errorhandler(404)
def page_not_found(error):
    return  jsonify({
        'message': 'Not found: the requested endpoint does not exist',
        'status': False
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'message': 'Serverside Error: an unexpected error occured',
        'status': False
    }), 500


@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({
        'message': "Unsupported media type: correct Content-Type 'application/json'",
        'status': False
    }), 415


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'message': 'Method not allowed: the http method is not accepted on this endpoint',
        'status': False
    }), 405

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'message': 'Bad request: failed to decode JSON object',
        'status': False
    }), 400
