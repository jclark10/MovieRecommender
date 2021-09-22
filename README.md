# Movie Recommender

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

## Features



