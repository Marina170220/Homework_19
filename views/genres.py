from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema

from implemented import genre_service
from service.auth import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{new_genre.id}"}


@genre_ns.route('/<int:gen_id>')
class GenreView(Resource):
    @auth_required
    def get(self, gen_id):
        r = genre_service.get_one(gen_id)
        return GenreSchema().dump(r), 200

    @admin_required
    def put(self, gen_id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gen_id
        if genre_service.update(req_json):
            return "", 204
        return "Genre not found", 404

    @admin_required
    def delete(self, gen_id):
        genre_service.delete(gen_id)
        return "", 204
