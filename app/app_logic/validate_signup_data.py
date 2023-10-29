from datetime import datetime

def validate_signup_data(json):
    response = {}
    firstname = json.get('firstname')
    lastname = json.get('lastname')
    middlename = json.get('middlename')
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')

    if not firstname or not lastname or not username or not email or not password:
        response['message'] = 'Missing required parameter'
        response['error'] = True
        response['error-code'] = 400
        return response
    
    response['firstname'] = firstname
    response['lastname'] = lastname
    response['middlename'] = middlename
    response['username'] = username
    response['email'] = email
    response['password'] = password
    response['created-at'] = datetime.now()
    return response
    