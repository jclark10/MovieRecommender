import pandas as pd
import numpy as np
from random import randrange
from nltk.corpus import wordnet
from nltk.wsd import lesk


class MovieLibrary:

    @staticmethod
    def read_in_string(info_str):
        info_list = info_str[2:-2].replace('\'', '').split(", ")
        return info_list

    def __init__(self):
        self.library_db = pd.read_csv('csv_data/movies_library.csv', low_memory=False)
        self.library_db['genres'] = self.library_db['genres'].apply(self.read_in_string)
        self.library_db['keywords'] = self.library_db['keywords'].apply(self.read_in_string)
        self.NUM_REC_MOVIES = 5

    def id_to_movie(self, id_):
        if id_ == 0:
            return self.get_random_movie()
        else:
            return self.library_db.loc[self.library_db['id'] == id_].squeeze()

    def title_to_movie(self, title):
        if title == "RANDOM":
            return self.get_random_movie()
        else:
            return self.library_db.loc[self.library_db['title'] == title].squeeze()

    def get_random_movie(self):
        rand_index = randrange(0, len(self.library_db))
        return self.library_db.iloc[[rand_index]].squeeze()

    @staticmethod
    def print_movie(movie):
        print("title ... " + str(movie['title']))
        print("    id ... " + str(movie['id']))
        print("    genre ... " + ", ".join(movie['genres']))
        print("    keywords ... " + ", ".join(movie['keywords']))

    @staticmethod
    def get_cs_list(kw_list):
        cs_list = list()
        for kw in kw_list:
            cs_list.append(lesk(kw_list, kw))
        return cs_list

    @classmethod
    def calculate_similarity(cls, kw_a, kw_b):
        if kw_a == [] or kw_b == []:
            return 1
        sm_matrix = list()
        cs_a_list = cls.get_cs_list(kw_a)
        cs_b_list = cls.get_cs_list(kw_b)
        for cs_a in cs_a_list:
            sm_row = list()
            for cs_b in cs_b_list:
                if cs_a is not None and cs_b is not None:
                    sm_row.append(wordnet.wup_similarity(cs_a, cs_b))
                else:
                    return 1
            sm_matrix.append(sm_row)
        return np.mean(sm_matrix)

    @staticmethod
    def check_movies_different(rec_origin_movie, compared_movie):
        different_movie = compared_movie['id'] != rec_origin_movie['id']
        if "AND" in rec_origin_movie['title']:
            different_movie = str(compared_movie['title']) not in str(rec_origin_movie['title'])
        return different_movie

    @staticmethod
    def check_genres_similar(rec_origin_movie, compared_movie):
        percent_cutoff = 3.0 / 4.0
        shared_genres = 0.0
        rec_genres = rec_origin_movie['genres']
        compared_genres = compared_movie['genres']
        for g_a in rec_genres:
            for g_b in compared_genres:
                if g_a == g_b:
                    shared_genres += 1.0
        similar_genres_percent = shared_genres / float(len(rec_genres))
        genre_check = similar_genres_percent > percent_cutoff
        return genre_check

    def get_recs_from_db(self, origin_movie):
        sm_total_list = list()
        movies_compared = 0
        for index, compared_movie in self.library_db.iterrows():
            title_is_string = isinstance(compared_movie['title'], str)
            different_movie = self.check_movies_different(origin_movie, compared_movie)
            similar_genres = self.check_genres_similar(origin_movie, compared_movie)
            if title_is_string and different_movie and similar_genres:
                temp_sm = self.calculate_similarity(
                    origin_movie['keywords'],
                    compared_movie['keywords'])
                movies_compared += 1
                print(movies_compared)
                if len(sm_total_list) < self.NUM_REC_MOVIES:
                    sm_total_list.append((compared_movie, temp_sm))
                elif temp_sm > sm_total_list[self.NUM_REC_MOVIES - 1][1]:
                    sm_total_list.append((compared_movie, temp_sm))
                    sm_total_list.sort(key=lambda x: x[1])
                    sm_total_list = sm_total_list[0:self.NUM_REC_MOVIES]
        sm_total_list = [movie_sm[0] for movie_sm in sm_total_list]
        recs_dataframe = pd.DataFrame(sm_total_list)
        return recs_dataframe

    def combine_movies(self, movie_a, movie_b):
        id_ = self.library_db['id'].max() + 1
        title = movie_a['title'] + " AND " + movie_b['title']
        genres = movie_a['genres'] + movie_b['genres']
        keywords = movie_a['keywords'] + movie_b['keywords']
        self.library_db.loc[len(self.library_db.index)] = [id_, title, genres, keywords]
        return self.id_to_movie(id_)

    def get_combined_recs(self, movie_a, movie_b):
        return self.get_recs_from_db(self.combine_movies(movie_a, movie_b))
