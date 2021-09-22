import json
import requests

BASE = "https://movie-library-recommender.herokuapp.com/"

# movie_id = "13"
# id_info_json = requests.get(BASE + "/MovieInfoAccess/" + movie_id).json()

movie_title = "42"
title_info_url = BASE + "MovieInfoAccess/" + movie_title
print(title_info_url)
title_info_json = requests.get(title_info_url).json()

title_info_dict = json.loads(title_info_json)
title_info_string = json.dumps(title_info_dict, indent=2)
print(title_info_string)


movie_title = str(title_info_dict["title"])
title_recs_url = BASE + "MovieRecommender/" + movie_title
print(title_recs_url)
title_recs_json = requests.get(title_recs_url).json()
title_recs_dict = json.loads(title_recs_json)
title_recs_string = json.dumps(title_recs_dict, indent=2)
print(title_recs_string)

# a_title = "Identity"
# b_title = "District 9"
# titles_couple_recs_json = requests.get(BASE + "/CoupleRecommender/" + a_title + "/" + b_title).json()
#
# couple_recs_dict = json.loads(titles_couple_recs_json)
# couple_recs_string = json.dumps(couple_recs_dict, indent=2)
# print(couple_recs_string)
