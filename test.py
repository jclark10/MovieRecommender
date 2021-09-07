import json
import requests

BASE = "http://127.0.0.1:5000/"

curr_movie_id = "0"
curr_movie_info = requests.get(BASE + "MovieAccess/" + curr_movie_id).json()
curr_json = json.loads(curr_movie_info)
print("title: " + str(curr_json['title']))
print("    genres: " + str(curr_json['genres']))
print("    keywords: " + str(curr_json['keywords']))
print("\n")
curr_movie_id = str(curr_json['id'])
movie_recs = requests.get(BASE + "MovieRecommender/" + curr_movie_id).json()
if movie_recs == "ERROR: NO RECOMMENDATIONS":
    print(movie_recs)
else:
    for i in movie_recs:
        movie_json = json.loads(i)
        print("title: " + str(movie_json['title']))
        print("    genres: " + str(movie_json['genres']))
        print("    keywords: " + str(movie_json['keywords']))
print("\n")

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
