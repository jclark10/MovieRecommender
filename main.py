from library import MovieLibrary
import time

movie_library = MovieLibrary()


def test_recommendations(movie_):
    print("~~ CURRENT MOVIE ~~")
    movie_library.print_movie(movie_)
    start_time = time.time()
    recommendations = movie_library.get_recs_from_db(movie_)
    print("~~ TIME TAKEN ~~")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("~~ RECOMMENDATIONS ~~")
    for rec_movie, sim_metric in recommendations:
        movie_library.print_movie(rec_movie)
        print("    similarity metric ... " + str(sim_metric))


movie_a = movie_library.get_random_movie()
# movie_library.print_movie(movie_a)
movie_b = movie_library.get_random_movie()
# movie_library.print_movie(movie_b)
combined_movie = movie_library.combine_movies(movie_a, movie_b)
test_recommendations(combined_movie)

# movie_c = movie_library.id_to_movie(78)
# movie_library.print_movie(movie_c)
