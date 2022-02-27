from flask import request, abort
from flask_restx import Namespace, Resource

from service.auth import login_user, refresh_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            abort(400)
        tokens = login_user(req_json)
        if tokens:
            return tokens, 200
        abort(401, "Authorization error")

    def put(self):
        req_json = request.json
        if not req_json:
            abort(400)
        tokens = refresh_token(req_json)
        if tokens:
            return tokens, 200
        abort(401, "Authorization error")
