import calendar
import datetime
import hashlib
import hmac
import base64

import jwt

from flask import request, abort

from constants import SECRET, ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from implemented import user_service


def auth_check():
    if 'Authorization' not in request.headers:
        return False
    token = request.headers['Authorization'].split("Bearer ")[-1]
    return jwt_decode(token)


def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, SECRET, ALGORITHM)
    except:
        return False
    else:
        return decoded_jwt


def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization error")

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_token = auth_check()
        if decoded_token:
            user_role = decoded_token.get('role')
            if user_role == 'admin':
                return func(*args, **kwargs)
        abort(401)

    return wrapper


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def compare_passwords(password_hash, entered_password):
    return hmac.compare_digest(base64.b64encode(password_hash),
                               hashlib.pbkdf2_hmac('sha256'), entered_password.encode('utf-8'),
                               PWD_HASH_SALT, PWD_HASH_ITERATIONS)


def login_user(req_json):
    user_name = req_json.get('username')
    user_password = req_json.get('password')
    if user_name and user_password:
        user = user_service.get_one_by_name(user_name)
        if user:
            hashed_password = user.password
            req_json['role'] = user.role
            if compare_passwords(hashed_password, user_password):
                return generate_token(req_json)
    return False


def refresh_token(req_json):
    refresh_token = req_json.get('refresh_token')
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    return False
