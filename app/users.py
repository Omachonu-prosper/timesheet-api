from flask import jsonify, Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from app_logic.connect_to_db import users
from app_logic.decorators import api_key_required

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
