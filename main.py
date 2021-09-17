from library import MovieLibrary

movie_library = MovieLibrary()
movie_a = movie_library.id_to_movie(28)
print(movie_a)
movie_a_recs = movie_library.get_recs_from_db(movie_a)
print(movie_a_recs)
