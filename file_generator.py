import pandas as pd
import datetime
from nltk.corpus import wordnet
from nltk.corpus import stopwords


def get_too_old_ids(mm_data, date_cutoff):
    ids = mm_data['id']
    release_dates = mm_data['release_date']
    output_ids = list()
    for curr_id, rd_str in zip(ids, release_dates):
        if not isinstance(rd_str, str):
            output_ids.append(curr_id)
        else:
            curr_dt = datetime.datetime(1800, 1, 1)
            if "/" in rd_str:
                rd_split = rd_str.split("/")
                year = int(rd_split[2])
                if year <= 18:
                    year = year + 2000
                else:
                    year = year + 1900
                month = int(rd_split[0])
                day = int(rd_split[1])
                curr_dt = datetime.datetime(year, month, day)
            elif "-" in rd_str:
                rd_split = rd_str.split("-")
                year = int(rd_split[0])
                month = int(rd_split[1])
                day = int(rd_split[2])
                curr_dt = datetime.datetime(year, month, day)
            if curr_dt <= date_cutoff:
                output_ids.append(curr_id)
    return output_ids


def delete_from_db_by_index(id_list, kw_data, mm_data):
    kw_index_list = list()
    mm_index_list = list()
    for curr_id in id_list:
        if curr_id in kw_data['id'].values:
            kw_index = kw_data.index[kw_data['id'] == curr_id].tolist()[0]
            kw_index_list.append(kw_index)
        if curr_id in mm_data['id'].values:
            mm_index = mm_data.index[mm_data['id'] == curr_id].tolist()[0]
            mm_index_list.append(mm_index)
    kw_data = kw_data.drop(kw_index_list)
    mm_data = mm_data.drop(mm_index_list)
    return kw_data, mm_data


# DATA INPUT AND FORMATTING
kw_db = pd.read_csv('csv_data/keywords.csv', low_memory=False)
movies_db = pd.read_csv('csv_data/movies_metadata.csv', low_memory=False)


# NARROWING DATABASES
def clean_databases(kw_db_, movies_db_):
    wanted_lang = 'en'
    is_not_english = movies_db_['original_language'] != wanted_lang
    not_english_ids = movies_db_[is_not_english]['id'].values
    kw_db_, movies_db_ = delete_from_db_by_index(
        not_english_ids,
        kw_db_,
        movies_db_)

    rd_cutoff = datetime.datetime(1975, 1, 1)
    too_old_ids = get_too_old_ids(movies_db_, rd_cutoff)
    kw_db_, movies_db_ = delete_from_db_by_index(
        too_old_ids,
        kw_db_,
        movies_db_)

    vote_count_cutoff = 300
    is_unpopular = movies_db_['vote_count'] <= vote_count_cutoff
    unpopular_ids = movies_db_[is_unpopular]['id'].values
    kw_db_, movies_db_ = delete_from_db_by_index(
        unpopular_ids,
        kw_db_,
        movies_db_)

    mm_ids = movies_db_['id'].values
    kw_ids = kw_db_['id'].values
    not_matching_ids = list()
    for curr_id_ in mm_ids:
        if curr_id_ not in kw_ids:
            not_matching_ids.append(curr_id_)
    for curr_id_ in kw_ids:
        if curr_id_ not in mm_ids:
            not_matching_ids.append(curr_id_)
    kw_db_, movies_db_ = delete_from_db_by_index(
            not_matching_ids,
            kw_db_,
            movies_db_)

    mm_ids = list(movies_db_['id'].values)
    kw_ids = list(kw_db_['id'].values)
    repeated_ids = list()
    for curr_id_ in mm_ids:
        if mm_ids.count(curr_id_) > 1:
            repeated_ids.append(curr_id_)
    for curr_id_ in kw_ids:
        if kw_ids.count(curr_id_) > 1:
            repeated_ids.append(curr_id_)
    kw_db_, movies_db_ = delete_from_db_by_index(
        repeated_ids,
        kw_db_,
        movies_db_)

    mm_ids = list(movies_db_['id'].values)
    mm_title = list(movies_db_['title'].values)
    kw_ids = list(kw_db_['id'].values)
    kw_kws = list(kw_db_['keywords'].values)
    title_not_string_ids = list()
    for curr_id, curr_title in zip(mm_ids, mm_title):
        if not isinstance(curr_title, str):
            title_not_string_ids.append(curr_id)
    for curr_id, curr_kws in zip(kw_ids, kw_kws):
        if not isinstance(curr_kws, str):
            title_not_string_ids.append(curr_id)
    kw_db_, movies_db_ = delete_from_db_by_index(
        title_not_string_ids,
        kw_db_,
        movies_db_)

    return kw_db_, movies_db_


kw_db, movies_db = clean_databases(kw_db, movies_db)


# CLEANING KEYWORDS AND GENRES
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
    return map(make_keywords_single, map(keyword_str_to_array, kw_data))


def reformat_single_feat(movie_info):
    return make_keywords_single(keyword_str_to_array(movie_info))


# GENERATING SMALLER DATABASE
def generate_new_database(movies_db_, kw_db_):
    limited_movies_db_ = movies_db_.filter(['id', 'title'], axis=1)
    just_genres_db_ = movies_db_.filter(['genres'], axis=1)
    just_genres_db_ = just_genres_db_.applymap(reformat_single_feat)
    limited_kw_db_ = kw_db_.filter(['keywords'], axis=1)
    limited_kw_db_ = limited_kw_db_.applymap(reformat_single_feat)
    combined_info_db_ = pd.concat([limited_movies_db_, just_genres_db_, limited_kw_db_], axis=1)
    combined_info_db_ = combined_info_db_.dropna(how='any', axis=0)
    return combined_info_db_


library_db = generate_new_database(movies_db, kw_db)


# GENERATING NEW CSV FILE
def generate_new_csv_file(db_):
    db_.to_csv('csv_data/movies_library.csv', index=False)


generate_new_csv_file(library_db)
