from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from service.auth import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        return DirectorSchema(many=True).dump(rs), 200

    @admin_required
    def post(self):
        req_json = request.json
        new_dir = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{new_dir.id}"}


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    @auth_required
    def get(self, dir_id):
        r = director_service.get_one(dir_id)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, dir_id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = dir_id
        if director_service.update(req_json):
            return "", 204
        return "Director not found", 404

    @admin_required
    def delete(self, dir_id):
        director_service.delete(dir_id)
        return "", 204



