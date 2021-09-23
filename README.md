# Movie Recommender API

This api is a movie recommendation system that bases its suggestions on an overlap of genres and a similarity in key plot words.
The api is also able to be given two movies and return suggestions that are similar to both of these movies.
This project allowed me to grow my skills with REST APIs and to experiment with natural language processing.
I used Python, Flask, Heroku, pandas and numpy and implemented natural language processing using the Natural Language Toolkit.
Specifically, I used wordnet for word similarity and lesk for word sense disambiguation.

The data set of movies is The Movies Dataset on Kaggle (https://www.kaggle.com/rounakbanik/the-movies-dataset)
I extracted a specific set of movies in order to make the dataset more manageable and applicable. 
I removed parts of the dataset that were broken or incomplete and only used english-language movies from after 1975 that had a large number of votes.
I saved the result as a csv file. 

The api is being hosted at https://movie-library-recommender.herokuapp.com/

## API FEATURES

**GET** https://movie-library-recommender.herokuapp.com/MovieInfoAccess/<string:movie_title>

INPUT: movie_title = the title of a movie

RETURN:  the information about movie named movie_title in the JSON format of {"id" : Movie_Id, "title" : Movie_Title, "genres" : Movie_Genres[], "keywords" : Movie_Keywords[]}

**GET** https://movie-library-recommender.herokuapp.com/MovieRecommender/<string:movie_title>

INPUT: movie_title = the title of a movie that the user wants recommendations for

RETURN: list of similar movies ranked in terms of their similarity to the genres and keywords of the input movie each in the JSON format of {"id" : Movie_Id, "title" : Movie_Title, "genres" : Movie_Genres[], "keywords" : Movie_Keywords[]} 

**GET** https://movie-library-recommender.herokuapp.com/CoupleRecommender/<string:title_a>/<string:title_b>

INPUT: title_a = title of the first movie for recommendations, title_b = title of the second movie for recommendations 

RETURN: list of similar movies ranked in terms of their similarity to the genres and keywords of a combination of two input movies each in the JSON format of {"id" : Movie_Id, "title" : Movie_Title, "genres" : Movie_Genres[], "keywords" : Movie_Keywords[]} 

## NOTES

I removed API functionality that allowed users to access movies via their id numbers.
Unique id numbers for each movie are included in the csv files and are used at certain points in my recommendation system.
I did this so that there would not be any confusion between id numbers and movie titles that are just numbers.
Examples include Roland Emmerich's 2012 and Brian Helgeland's 42.
If I build a solution to this problem in the future, I will be sure to return access to these API routes. 

## Possible Future Additions

- Refining the genre overlap metric and the keywords similarity metric
- Speeding up the process for finding suggestions
- Allowing for a list of movies to be sent to the Movie Recommender, instead of just 1 or 2


