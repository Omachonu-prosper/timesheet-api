from flask import jsonify, Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from app_logic.connect_to_db import users
from app_logic.decorators import api_key_required
from app_logic.parser import ParsePayload

users_bp = Blueprint('users', __name__)


@users_bp.route('/user/account/personal-information', strict_slashes=False)
@api_key_required
@jwt_required()
def personal_info():
    user_id = get_jwt_identity()
    user = users.find_one(
        {'_id': ObjectId(user_id)},
        {'reports': 0, '_id': 0, 'password': 0, 'created-at': 0}
    )
    if not user:
        return jsonify({
            'message': 'Not found: no data found for the requested user',
            'status': False
        }), 404
    
    return jsonify({
        'message': 'Account information fetched successfully',
        'status': True,
        'data': user
    }), 200


@users_bp.route('/user/account/personal-information/name', methods=['PUT'], strict_slashes=False)
@api_key_required
@jwt_required()
def edit_name():
    parser = ParsePayload(request.json)
    parser.add_args('firstname', True, 'firstname cannot be blank')
    parser.add_args('middlename')
    parser.add_args('lastname', True, 'lastname cannot be blank')
    
    if not parser.valid:
        return parser.generate_errors('Missing required parameter')
    
    user_id = get_jwt_identity()
    data = parser.args
    user = users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'firstname': data['firstname'],
            'middlename': data['middlename'],
            'lastname': data['lastname']
        }}
    )
    if user.matched_count:
        return jsonify({
            'message': 'Account info updated successfully',
            'status': True,
        }), 200
    else:
        return jsonify({
            'message': 'Not found: no data found for the requested user',
            'status': False,
        }), 404