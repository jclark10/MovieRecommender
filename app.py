from flask import Flask
from flask_restful import Api, Resource
from library import MovieLibrary

movie_library = MovieLibrary()
app = Flask(__name__)
api = Api(app)


class status(Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}, 200
        except:
            return {'data': 'An Error Occurred during fetching Api'}, 404


class MovieIdAccess(Resource):
    def get(self, movie_id):
        movie_info = movie_library.id_to_movie(movie_id)
        if movie_info.empty:
            return {'data': 'ERROR: NO MOVIE WITH CURRENT ID'}, 404
        else:
            return movie_info.to_json(), 200


class MovieTitleAccess(Resource):
    def get(self, movie_title):
        movie_info = movie_library.title_to_movie(movie_title)
        if movie_info.empty:
            return {'data': 'ERROR: NO MOVIE WITH CURRENT TITLE'}, 404
        else:
            return movie_info.to_json(), 200


class MovieIdRecommender(Resource):
    def get(self, movie_id):
        curr_movie = movie_library.id_to_movie(movie_id)
        movie_recs = movie_library.get_recs_from_db(curr_movie)
        if movie_recs.empty:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            return movie_recs.to_json(orient='records'), 200


class MovieTitleRecommender(Resource):
    def get(self, movie_title):
        curr_movie = movie_library.title_to_movie(movie_title)
        movie_recs = movie_library.get_recs_from_db(curr_movie)
        if movie_recs.empty:
            print("HITS EMPTY RETURN")
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            print("HITS INFO RETURN")
            return movie_recs.to_json(orient='records'), 200


class CoupleIdRecommender(Resource):
    def get(self, id_a, id_b):
        movie_a = movie_library.id_to_movie(id_a)
        movie_b = movie_library.id_to_movie(id_b)
        movie_recs = movie_library.get_combined_recs(movie_a, movie_b)
        if movie_recs.empty:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            return movie_recs.to_json(orient='records'), 200


class CoupleTitleRecommender(Resource):
    def get(self, title_a, title_b):
        movie_a = movie_library.title_to_movie(title_a)
        movie_b = movie_library.title_to_movie(title_b)
        movie_recs = movie_library.get_combined_recs(movie_a, movie_b)
        if movie_recs.empty:
            return {'data': 'ERROR: NO RECOMMENDATIONS FOUND'}, 404
        else:
            return movie_recs.to_json(orient='records'), 200


# BASE = "https://movie-library-recommender.herokuapp.com"
api.add_resource(status, "/")

api.add_resource(MovieTitleAccess, "/MovieInfoAccess/<string:movie_title>")
api.add_resource(MovieTitleRecommender, "/MovieRecommender/<string:movie_title>")
api.add_resource(CoupleTitleRecommender, "/CoupleRecommender/<string:title_a>/<string:title_b>")

# api.add_resource(MovieIdAccess, "/MovieInfoAccess/<int:movie_id>")
# api.add_resource(MovieIdRecommender, "/MovieRecommender/<int:movie_id>")
# api.add_resource(CoupleIdRecommender, "/CoupleRecommender/<int:id_a>/<int:id_b>")

if __name__ == "__main__":
    app.run(debug=True)
