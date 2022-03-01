import calendar
import datetime
import hashlib
import hmac
import base64

from flask import request, abort
import jwt

from constants import SECRET, ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from implemented import user_service


def check_token(token):
    """
    Проверка актуальности токена.
    Return: декодированный токен.
    """
    try:
        decoded_jwt = jwt.decode(token, SECRET, ALGORITHM)
    except:
        return False
    else:
        return decoded_jwt


def auth_check():
    """
    Проверка авторизации пользователя. Если пользователь авторизовался возвращаем токен.
    Return: результат проверки токена.
    """
    if 'Authorization' not in request.headers:
        return False
    token = request.headers['Authorization'].split("Bearer ")[-1]
    return check_token(token)


def auth_required(func):
    """
    Декоратор, проверяющий авторизацию пользователя.
    """
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization error")

    return wrapper


def admin_required(func):
    """
    Декоратор, проверяющий права пользователя.
    """
    def wrapper(*args, **kwargs):
        decoded_token = auth_check()
        if decoded_token:
            user_role = decoded_token.get('role', 'user')
            if user_role != 'admin':
                abort(403)
            return func(*args, **kwargs)
        abort(401)

    return wrapper


def generate_token(data):
    """
    Генерируем access и refresh токены.
    """
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def compare_passwords(password_hash, entered_password):
    """
    Сравниваем пароли пользователя.
    Param password_hash: захешированный пароль из БД.
    Param entered_password: пароль в чистом виде, полученный из реквеста.
    Return: результат сравнения паролей в бинарном представлении.

    """
    decoded_digest = base64.b64decode(password_hash)
    hash_digest = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'),
                                      PWD_HASH_SALT, PWD_HASH_ITERATIONS)

    return hmac.compare_digest(decoded_digest, hash_digest)


def login_user(req_json):
    """
    Авторизация пользователя и получение токенов.
    Param req_json: данные пользователя в json-формате.
    Return: access и refresh токены либо False в случае, если отсутствуют имя и/или пароль пользователя.
    """
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
    """
    Получение новой пары токенов.
    """
    refresh_token = req_json.get('refresh_token')
    data = check_token(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    return False
