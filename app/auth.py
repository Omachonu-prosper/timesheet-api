"""
Authentication related routes (Login and signup)
"""

import os
from flask import request, jsonify, Blueprint
from dotenv import load_dotenv
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

# App logic dependencies
from app_logic.connect_to_db import users, admins
from app_logic.decorators import api_key_required, admin_protected
from app_logic.generate_employee_id import generate_employee_id
from app_logic.generate_verification_string import generate_verification_string
from app_logic.parser import ParsePayload

# Create a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)
load_dotenv()
BASE_URL = os.getenv('BASE_URL', None)


@auth.route('/admin/login', methods=['POST'], strict_slashes=False)
@api_key_required
def admin_login():
    parser = ParsePayload(request.json)
    parser.add_args('username', True, 'Username must be provided')
    parser.add_args('password', True, 'password must be provided')
    if not parser.valid:
        return parser.generate_errors('Missing required parameter')
    
    data = parser.args
    username = data.get('username', None)
    password = data.get('password', None)
    admin = admins.find_one(
        {"username": username, "password": password},
        {"_id": 1}
    )
    if admin is None:
        return jsonify({
            'message': 'Login failed: invalid credentials',
            'status': False
        }), 404
    
    admin_id = str(admin['_id'])
    token = create_access_token(identity=admin_id)
    response = {
        'access_token': token,
        'message': 'Login successful',
        'data': None,
        'status': True
    }
    return jsonify(response), 200


@auth.route('/user/login', methods=['POST'], strict_slashes=False)
@api_key_required
def login():
    parser = ParsePayload(request.json)
    parser.add_args('email', True, 'email must be provided')
    parser.add_args('password', True, 'password must be provided')
    if not parser.valid:
        return parser.generate_errors('Missing required parameter')
    
    data = parser.args
    email = data.get('email', None)
    password = data.get('password', None)
    user = users.find_one(
        {'email': email},
        {'_id': 1, 'password': 1}
    )
    if user is None:
        return jsonify({
            'message': 'Failed to log user in: email not found',
            'status': False
        }), 404
    
    password_matchs = check_password_hash(user['password'], password)
    if not password_matchs:
        return jsonify({
            'message': 'Failed to log user in: invalid credentials',
            'status': False
        }), 404
        
    user_id = str(user['_id'])
    token = create_access_token(identity=user_id)
    response = {
        'access_token': token,
        'message': 'Login successful',
        'user-id': user_id,
        'data': None,
        'status': True
    }
    return jsonify(response)


@auth.route('/user/signup', methods=['POST'], strict_slashes=False)
@api_key_required
@jwt_required()
@admin_protected
def signup():
    parser = ParsePayload(request.json)
    parser.add_args('email', True, 'email must be provided')
    parser.add_args('firstname', True, 'firstname must be provided')
    parser.add_args('lastname', True, 'lastname must be provided')
    if not parser.valid:
        return parser.generate_errors('Missing required parameter')
    
    data = parser.args
    email = data.get('email', None)

    # Check if a user with the email already exists
    user = users.find_one(
        {"email": email},
        {"_id": 1}
    )
    if user is not None:
        return jsonify({
            'message': 'Failed to create user: email is taken',
            'status': False
        }), 409
    
    # # Check if a user with the username already exists
    # user = users.find_one(
    #     {"username": username},
    #     {"_id": 1}
    # )
    # if user is not None:
    #     return jsonify({
    #         'message': 'Failed to create user: username is taken',
    #         'status': False
    #     }), 409

    data['employee-id'] = generate_employee_id()
    data['verification-string'] = generate_verification_string()
    data['activated'] = False
    insert = users.insert_one(data)
    user_id = str(insert.inserted_id)
    if not insert.acknowledged:
        return jsonify({
            'message': 'Failed to create user: an error occured',
            'status': False
        }), 500
    
    response = {
        'message': "User created successfully",
        'data': {
            'employee-id': data['employee-id'],
            'user-id': user_id,
            'activation-link': f"{BASE_URL}/user/account/activate/{user_id}/{data['verification-string']}",
            'email': data['email']
        },
        'status': True
    }
    return response, 201


@auth.route('/user/account/activate', methods=['POST'], strict_slashes=False)
def activate_account():
    return "under construction"