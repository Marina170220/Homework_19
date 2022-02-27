from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema

from implemented import movie_service
from service.auth import auth_required, admin_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{new_movie.id}"}


@movie_ns.route('/<int:mov_id>')
class MovieView(Resource):
    @auth_required
    def get(self, mov_id):
        b = movie_service.get_one(mov_id)
        return MovieSchema().dump(b), 200

    @admin_required
    def put(self, mov_id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = mov_id
        if movie_service.update(req_json):
            return "", 204
        return "Movie not found", 404

    @admin_required
    def delete(self, mov_id):
        movie_service.delete(mov_id)
        return "", 204
