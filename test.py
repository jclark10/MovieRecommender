import json
import requests

BASE = "https://movie-library-recommender.herokuapp.com/"

movie_id = "13"
movie_title = "Forrest Gump"
id_info_json = requests.get(BASE + "MovieInfoAccess/" + movie_id).json()
title_info_json = requests.get(BASE + "MovieInfoAccess/" + movie_title).json()
# print(id_info_json == title_info_json)

id_info_dict = json.loads(id_info_json)
movie_id = str(id_info_dict["id"])
title_info_dict = json.loads(title_info_json)
movie_title = str(title_info_dict["title"])
id_recs_json = requests.get(BASE + "MovieRecommender/" + movie_id).json()
title_recs_json = requests.get(BASE + "MovieRecommender/" + movie_title).json()
# print(id_recs_json == title_recs_json)

# info_json_formatted_str = json.dumps(id_info_dict, indent=2)
# print(info_json_formatted_str)
# recs_dict = json.loads(id_recs_json)
# recs_json_formatted_str = json.dumps(recs_dict, indent=2)
# print(recs_json_formatted_str)


a_id = "2832"
a_title = "Identity"

b_id = "17654"
b_title = "District 9"

id_couple_recs_json = requests.get(BASE + "CoupleRecommender/" + a_id + "/" + b_id).json()
titles_couple_recs_json = requests.get(BASE + "CoupleRecommender/" + a_title + "/" + b_title).json()

couple_recs_dict = json.loads(id_couple_recs_json)
couple_recs_string = json.dumps(couple_recs_dict, indent=2)
print(couple_recs_string)
