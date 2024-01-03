"""
Authentication related routes (Login and signup)
"""

import os
from datetime import datetime
from flask import request, jsonify, Blueprint
from dotenv import load_dotenv
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

# App logic dependencies
from core import app
from core.utils.connect_to_db import users, admins
from core.utils.decorators import api_key_required, admin_protected
from core.utils.generate_employee_id import generate_employee_id
from core.utils.generate_verification_code import generate_verification_code
from core.utils.parser import ParsePayload

# Create a Blueprint for the authentication routes
load_dotenv()

@app.route('/admin/login', methods=['POST'], strict_slashes=False)
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


@app.route('/user/login', methods=['POST'], strict_slashes=False)
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
        {'_id': 1, 'password': 1, 'activated': 1}
    )
    if user is None:
        return jsonify({
            'message': 'Failed to log user in: email not found',
            'status': False
        }), 404
    elif user.get('password', None) is None and user.get('activated', False) == False:
        return jsonify({
            'message': 'Failed to log user in: please activate your account to login',
            'status': False
        }), 401
    
    password_matchs = check_password_hash(user['password'], password)
    if not password_matchs:
        return jsonify({
            'message': 'Failed to log user in: invalid credentials',
            'status': False
        }), 401
        
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


@app.route('/user/signup', methods=['POST'], strict_slashes=False)
@api_key_required
def signup():
    parser = ParsePayload(request.json)
    parser.add_args('email', True, 'email must be provided')
    parser.add_args('firstname', True, 'firstname must be provided')
    parser.add_args('middlename', True, 'middlename is optional')
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

    data['employee-id'] = generate_employee_id()
    data['verification-code'] = generate_verification_code()
    data['activated'] = False
    data['created-at'] = datetime.now()
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
            'verification-code': data['verification-code'],
            'user-id': user_id,
            'email': data['email']
        },
        'status': True
    }
    return response, 201


@app.route('/user/account/activate', methods=['POST'], strict_slashes=False)
def activate_account():
    parser = ParsePayload(request.json)
    parser.add_args('password', True, 'password must be provided')
    parser.add_args('email', True, 'email must be provided')
    parser.add_args('verification-code', True, 'verification-code must be provided')
    if not parser.valid:
        return parser.generate_errors('Missing required parameter')
    
    data = parser.args
    password = generate_password_hash(data.get('password', None))
    email = data.get('email', None)
    verification_code = data.get('verification-code', None)

    user = users.find_one({'email': email}, {'_id': 1})
    user_id = str(user['_id'])
    if not user:
        return jsonify({
            'message': 'Not found: check the email submitted',
            'status': False
        }), 404
    
    user = users.update_one(
        {'email': email, 'verification-code': verification_code},
        {'$set': {'password': password, 'activated': True, 'verification-code': None, 'activated-at': datetime.now()}}
    )
    if not user.matched_count:
        return jsonify({
            'message': 'Invalid code: check the verification code submitted',
            'status': False
        }), 400
    
    token = create_access_token(identity=user_id)
    return jsonify({
        'message': 'Account activated successfully',
        'status': True,
        'user-id': user_id,
        'access_token': token
    })