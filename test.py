import json
import requests

BASE = "https://movie-library-recommender.herokuapp.com/"

# TESTING ID ACCESS
curr_movie_id = "Raiders of the Lost Ark"
movie_info_json = requests.get(BASE + "MovieInfoAccess/" + curr_movie_id).json()
print(movie_info_json)
print("\n")
movie_info_dict = json.loads(movie_info_json)
curr_movie_id = str(movie_info_dict["id"])
print(curr_movie_id)
print("\n")
movie_recs_json = requests.get(BASE + "MovieRecommender/" + curr_movie_id).json()
print(movie_recs_json)