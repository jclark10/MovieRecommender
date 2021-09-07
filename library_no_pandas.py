import pandas as pd
import numpy as np
from movie import Movie
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.wsd import lesk
from random import randrange


# HELPER FUNCTIONS
def validate_word(word):
    in_wordnet = wordnet.synsets(word)
    not_stopword = word not in set(stopwords.words('english'))
    not_short = len(word) >= 3
    return in_wordnet and not_stopword and not_short


def keyword_str_to_array(kw_str):
    if not isinstance(kw_str, str) or len(kw_str) <= 2:
        return list()
    kw_str = kw_str[8: -2]
    kw_arr = kw_str.split("}, {")
    for i in range(len(kw_arr)):
        kw_arr[i] = kw_arr[i].replace("'id': ", "")
        kw_arr[i] = kw_arr[i].replace("name': ", "")
        kw_arr[i] = kw_arr[i].split(", '")
        kw_arr[i] = kw_arr[i][1].replace("\'", "")
        kw_arr[i] = kw_arr[i].replace("\"", "")
    return kw_arr


def make_keywords_single(kws):
    solo_kws = list()
    for kw in kws:
        split_phrase = kw.split(" ")
        for word_ in split_phrase:
            if validate_word(word_):
                solo_kws.append(word_)
            else:  # dealing with compound words
                for i in range(len(word_)):
                    sub_a = word_[0:i]
                    sub_b = word_[i:]
                    if validate_word(sub_a) and validate_word(sub_b):
                        solo_kws.append(sub_a)
                        solo_kws.append(sub_b)
    return solo_kws


def reformat_movie_features(kw_data):
    return list(map(make_keywords_single, map(keyword_str_to_array, kw_data)))


# MOVIE LIBRARY CLASS
class MovieLibrary:
    def __init__(self):
        self.loaded_in = False
        library_db = pd.read_csv('csv_data/movies_library.csv', low_memory=False)
        ids_ = library_db['id'].values
        titles = library_db['title'].values
        kw_list = reformat_movie_features(library_db["keywords"].values)
        genre_list = reformat_movie_features(library_db['genres'].values)

        zipped_data = zip(ids_, titles, kw_list, genre_list)
        self.entries = list()
        self.highest_id_ = 0
        for id_, title, keywords, genres in zipped_data:
            if str(id_) != "nan" and str(title) != "nan":
                self.entries.append(Movie(id_, title, keywords, genres))
            if id_ > self.highest_id_:
                self.highest_id_ = id_
        self.loaded_in = True

    def id_to_movie(self, id_):
        for movie in self.entries:
            if movie.id_ == id_:
                return movie

    # may not always be accurate
    def title_to_movie(self, title):
        for movie in self.entries:
            if movie.title == title:
                return movie

    def get_new_index(self):
        new_id_ = self.highest_id_ + 1
        self.highest_id_ = new_id_
        return new_id_

    def add_movie(self, movie_):
        self.entries.append(movie_)

    def get_random_movie(self):
        rand_index = randrange(0, len(self.entries))
        return self.entries[rand_index]

    def get_libraries(self):
        return self.entries

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
        for temp_movie in self.entries:
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
        id_ = self.get_new_index()
        title = str(movie_a.title) + " AND " + str(movie_b.title)
        genres = movie_a.genres + movie_b.genres
        keywords = movie_a.keywords + movie_b.keywords
        combined_movie = Movie(id_, title, keywords, genres)
        self.add_movie(combined_movie)
        return combined_movie

    def get_combined_recs(self, movie_a, movie_b):
        return self.get_recs_from_db(self.combine_movies(movie_a, movie_b))
