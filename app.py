from flask import Flask, redirect, url_for, request, render_template
from library import MovieLibrary

movie_library = MovieLibrary()
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/movie_info', methods=['GET', 'POST'])
def print_movie_info():
    if request.method == 'POST':
        if 'RandomMovieButton' in request.form:
            curr_id = movie_library.get_random_id()
        else:
            curr_id = float(request.form['movie_id'])
        movie_a = movie_library.id_to_movie(curr_id)
        recommendations = movie_library.get_recs_from_db(movie_a)
        return render_template('movie_info.html',
                               movie=movie_a,
                               recs=recommendations)


@app.route('/', methods=['POST', 'GET'])
def submit_id():
    if request.method == 'POST':
        if request.form['HomeButton'] == 'Return Home':
            return render_template('submit_id.html')
    return render_template('submit_id.html')


# main driver function
if __name__ == '__main__':
    if movie_library.loaded_in:
        app.run()
        # 607 id = Men in Black
