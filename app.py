from flask import Flask, jsonify
from flask_restful import Api, Resource
from library import MovieLibrary
import json
from pandas.io.json import to_json

movie_library = MovieLibrary()
app = Flask(__name__)
api = Api(app)


class status(Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}


class MovieIdAccess(Resource):
    def get(self, movie_id):
        movie_info = movie_library.id_to_movie(movie_id)
        if movie_info.empty:
            return {'data': 'ERROR: NO MOVIE WITH CURRENT ID'}, 404
        else:
            # return movie_info.to_json(), 200
            movie_json = jsonify(movie_info.to_json(orient='records'))
            return movie_json


class MovieTitleAccess(Resource):
    def get(self, movie_title):
        movie_info = movie_library.title_to_movie(movie_title)
        if movie_info.empty:
            return {'data': 'ERROR: NO MOVIE WITH CURRENT TITLE'}, 404
        else:
            return movie_info.to_json(), 200


class MovieRecommender(Resource):
    def get(self, movie_id):
        curr_movie = movie_library.id_to_movie(movie_id)
        movie_recs = movie_library.get_recs_from_db(curr_movie)
        if movie_recs.empty:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            return movie_recs.to_json(orient='records'), 200


class CoupleRecommender(Resource):
    def get(self, id_a, id_b):
        movie_a = movie_library.id_to_movie(id_a)
        movie_b = movie_library.id_to_movie(id_b)
        movie_recs = movie_library.get_combined_recs(movie_a, movie_b)
        if movie_recs.empty:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            return movie_recs.to_json(orient='records'), 200


api.add_resource(status, "/")
api.add_resource(MovieIdAccess, "/MovieIdAccess/<int:movie_id>")
api.add_resource(MovieTitleAccess, "/MovieTitleAccess/<string:movie_title>")
api.add_resource(MovieRecommender, "/MovieRecommender/<int:movie_id>")
api.add_resource(CoupleRecommender, "/CoupleRecommender/<int:id_a>/<int:id_b>")

if __name__ == "__main__":
    app.run(debug=True)
