# MOVIE CLASS
class Movie:
    def __init__(self, id_, title, keywords, genres):
        self.id_ = id_
        self.title = title
        if keywords == list():
            self.keywords = genres
        else:
            self.keywords = keywords
        self.genres = genres

    def get_id_(self):
        return self.id_

    def get_title(self):
        return self.title

    def get_keywords(self):
        return self.keywords

    def get_genres(self):
        return self.genres

    def print_movie(self):
        print("title ... " + str(self.title))
        print("id ... " + str(self.id_))
        print("genre ... " + ", ".join(self.genres))
        print("keywords ... " + ", ".join(self.keywords))
        print("\n")

    def get_movie_string(self):
        title = "title ... " + str(self.title) + "<br>"
        id = "id ... " + str(self.id_) + "<br>"
        genres = "genres ... " + ", ".join(self.genres) + "<br>"
        keywords = "keywords ... " + ", ".join(self.keywords) + "<br>"
        return "<p>" + title + id + genres + keywords + "</p>"
