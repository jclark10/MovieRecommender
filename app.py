from flask import Flask
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
        if movie_id == 0:
            return movie_library.get_random_movie().to_json()
        else:
            movie_info = movie_library.id_to_movie(movie_id)
            if movie_info.empty:
                return {'data': 'ERROR: NO MOVIE WITH CURRENT ID'}
            else:
                return movie_info.to_json()


class MovieTitleAccess(Resource):
    def get(self, movie_title):
        if movie_title == "RANDOM":
            return movie_library.get_random_movie().to_json()
        else:
            movie_info = movie_library.title_to_movie(movie_title)
            if movie_info.empty:
                return {'data': 'ERROR: NO MOVIE WITH CURRENT TITLE'}
            else:
                return movie_info.to_json()


class MovieRecommender(Resource):
    def get(self, movie_id):
        if movie_id == 0:
            curr_movie = movie_library.get_random_movie()
        else:
            curr_movie = movie_library.id_to_movie(movie_id)
        movie_recs = movie_library.get_recs_from_db(curr_movie)
        if len(movie_recs) == movie_library.NUM_REC_MOVIES:
            mr_list = list()
            for rec in movie_recs:
                mr_list.append(rec.to_json())
            return mr_list
        else:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}


class CoupleRecommender(Resource):
    def get(self, id_a, id_b):
        if id_a == 0:
            movie_a = movie_library.get_random_movie()
        else:
            movie_a = movie_library.id_to_movie(id_a)
        if id_b == 0:
            movie_b = movie_library.get_random_movie()
        else:
            movie_b = movie_library.id_to_movie(id_a)
        movie_recs = movie_library.get_combined_recs(movie_a, movie_b)
        if len(movie_recs) == movie_library.NUM_REC_MOVIES:
            mr_list = list()
            for rec in movie_recs:
                mr_list.append(rec.to_json())
            return mr_list
        else:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}


api.add_resource(status, "/")
api.add_resource(MovieIdAccess, "/MovieIdAccess/<int:movie_id>")
api.add_resource(MovieTitleAccess, "/MovieTitleAccess/<string:movie_title>")
api.add_resource(MovieRecommender, "/MovieRecommender/<int:movie_id>")
api.add_resource(CoupleRecommender, "/CoupleRecommender/<int:id_a>/<int:id_b>")

if __name__ == "__main__":
    app.run(debug=True)
