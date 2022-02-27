import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_one_by_name(self, user_name):
        return self.dao.get_one_by_name(user_name)

    def create(self, data):
        user_password = data.get('password')
        if user_password:
            data['password'] = get_hash(user_password)
        return self.dao.create(data)

    def update(self, data):
        user = self.get_one(data.get('id'))
        if user:
            if data.get('username'):
                user.username = data.get('username')
            if data.get('password'):
                data['password'] = get_hash(user.password)
                user.password = data.get('password')
            if data.get('role'):
                user.role = data.get('role')
            return self.dao.update(data)
        return None

    def delete(self, uid):
        return self.dao.delete(uid)


def get_hash(password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
