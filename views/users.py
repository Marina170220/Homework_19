from flask import request
from flask_restx import Namespace, Resource

from implemented import user_service
from dao.model.user import UserSchema

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        if users:
            return UserSchema(many=True).dump(users), 200
        return "Not found", 404

    def post(self):
        req_json = request.json
        new_user = user_service.create(req_json)
        return f"User id {new_user.id} created", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid: int):
        user = user_service.get_one(uid)
        if user:
            return UserSchema().dump(user), 200
        return "User not found", 404

    def put(self, uid: int):
        req_json = request.json
        if "id" not in req_json:
            req_json['id'] = uid
        if user_service.update(req_json):
            return f"{uid} updated", 201
        return "User not found", 404

    def delete(self, uid: int):
        user_service.delete(uid)
        return "", 204
