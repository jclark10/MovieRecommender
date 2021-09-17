import json
import requests

# BASE = "http://127.0.0.1:5000/" LOCAL SERVER TESTING
BASE = "https://movie-library-recommender.herokuapp.com/"

# TESTING ID ACCESS
curr_movie_id = "0"
movie_info_json = requests.get(BASE + "MovieIdAccess/" + curr_movie_id).json()
print(movie_info_json)
movie_info_dict = json.loads(movie_info_json)
curr_movie_id = str(movie_info_dict['id'])
print("id: " + curr_movie_id)
movie_recs_json = requests.get(BASE + "MovieRecommender/" + curr_movie_id).json()
print(movie_recs_json)

# if curr_movie_info == "ERROR: NO MOVIE WITH CURRENT ID":
#     print(curr_movie_info)
# else:
#     curr_json = json.loads(curr_movie_info)
#     print("title: " + str(curr_json['title']))
#     print("    genres: " + str(curr_json['genres']))
#     print("    keywords: " + str(curr_json['keywords']))
#     print("\n")
#     curr_movie_id = str(curr_json['id'])
#     movie_recs = requests.get(BASE + "MovieRecommender/" + curr_movie_id).json()
#     json_info = json.loads(movie_recs)
#     if json_info['data'] == 'ERROR: NO RECOMMENDATIONS FOUND':
#         print(movie_recs)
#     else:
#         for index, curr_movie in enumerate(movie_recs):
#             movie_json = json.loads(curr_movie)
#             print("~~ NUMBER " + str(index + 1) + " ~~")
#             print("title: " + str(movie_json['title']))
#             print("    genres: " + str(movie_json['genres']))
#             print("    keywords: " + str(movie_json['keywords']))
# print("\n")

# TESTING TITLE ACCESS
# curr_movie_title = "RANDOM"
# curr_movie_info = requests.get(BASE + "MovieTitleAccess/" + curr_movie_title).json()
# if curr_movie_info == "ERROR: NO MOVIE WITH CURRENT TITLE":
#     print(curr_movie_info)
# else:
#     curr_json = json.loads(curr_movie_info)
#     print("title: " + str(curr_json['title']))
#     print("    genres: " + str(curr_json['genres']))
#     print("    keywords: " + str(curr_json['keywords']))
#     print("\n")
#     curr_movie_id = str(curr_json['id'])
#     movie_recs = requests.get(BASE + "MovieRecommender/" + curr_movie_id).json()
#     if movie_recs['data'] == 'ERROR: NO RECOMMENDATIONS FOUND':
#         print(movie_recs)
#     else:
#         for index, curr_movie in enumerate(movie_recs):
#             movie_json = json.loads(curr_movie)
#             print("~~ NUMBER " + str(index + 1) + " ~~")
#             print("title: " + str(movie_json['title']))
#             print("    genres: " + str(movie_json['genres']))
#             print("    keywords: " + str(movie_json['keywords']))
# print("\n")

# id_a = "627"
# id_b = "810"
# id_a = "0"
# id_b = "0"
# movie_a_info = requests.get(BASE + "MovieAccess/" + id_a).json()
# movie_b_info = requests.get(BASE + "MovieAccess/" + id_b).json()
# a_json = json.loads(movie_a_info)
# print("title: " + str(a_json['title']))
# print("    genres: " + str(a_json['genres']))
# print("    keywords: " + str(a_json['keywords']))
# b_json = json.loads(movie_b_info)
# print("title: " + str(b_json['title']))
# print("    genres: " + str(b_json['genres']))
# print("    keywords: " + str(b_json['keywords']))
# print("\n")
# id_a = str(a_json['id'])
# id_b = str(b_json['id'])
# movie_recs = requests.get(BASE + "CoupleRecommender/" + id_a + "/" + id_b).json()
# if movie_recs == "ERROR: NO RECOMMENDATIONS":
#     print(movie_recs)
# else:
#     for i in movie_recs:
#         movie_json = json.loads(i)
#         print("title: " + str(movie_json['title']))
#         print("    genres: " + str(movie_json['genres']))
#         print("    keywords: " + str(movie_json['keywords']))
# print("\n")
