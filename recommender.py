import numpy as np
from movie import Movie
from library import MovieLibrary
from nltk.corpus import wordnet
from nltk.wsd import lesk


# MOVIE RECOMMENDER CLASS
class MovieRecommender:
    @staticmethod
    def get_cs_list(kw_list):
        cs_list = list()
        for kw in kw_list:
            cs_list.append(lesk(kw_list, kw))
        return cs_list

    @classmethod
    def calculate_similarity(cls, movie_a, movie_b):
        if movie_a.keywords == [] or movie_b.keywords == []:
            return 1
        sm_matrix = list()
        cs_a_list = cls.get_cs_list(movie_a.keywords)
        cs_b_list = cls.get_cs_list(movie_b.keywords)
        for cs_a in cs_a_list:
            sm_row = list()
            for cs_b in cs_b_list:
                sm_row.append(wordnet.wup_similarity(cs_a, cs_b))
            sm_matrix.append(sm_row)
        return np.mean(sm_matrix)

    def get_recs_from_db(self, input_movie):
        sm_total_list = list()
        for temp_movie in self.library.entries:
            if isinstance(temp_movie.title, str):
                different_movie = temp_movie.id_ != input_movie.id_
                if "AND" in input_movie.title:
                    different_movie = str(temp_movie.title) not in str(input_movie.title)

                percent_cutoff = float(3 / 4)
                shared_genres_count = len(set(temp_movie.genres) & set(input_movie.genres))
                total_genres_count = float(len(set(temp_movie.genres) | set(input_movie.genres)))
                similar_genres_percent = float(shared_genres_count / total_genres_count)
                genre_check = similar_genres_percent >= percent_cutoff

                if different_movie and genre_check:
                    temp_sm = self.calculate_similarity(
                        input_movie,
                        temp_movie)
                    if len(sm_total_list) <= 10:
                        sm_total_list.append((temp_movie, temp_sm))
                    elif temp_sm >= sm_total_list[9][1]:
                        sm_total_list.append((temp_movie, temp_sm))
                        sm_total_list.sort(key=lambda x: x[1])
                        sm_total_list = sm_total_list[0:10]
        return sm_total_list[0:5]

    def combine_movies(self, movie_a, movie_b):
        id_ = self.library.get_new_index()
        title = str(movie_a.title) + " AND " + str(movie_b.title)
        genres = movie_a.genres + movie_b.genres
        keywords = movie_a.keywords + movie_b.keywords
        combined_movie = Movie(id_, title, keywords, genres)
        self.library.add_movie(combined_movie)
        return combined_movie

    def get_combined_recs(self, movie_a, movie_b):
        return self.get_recs_from_db(self.combine_movies(movie_a, movie_b))