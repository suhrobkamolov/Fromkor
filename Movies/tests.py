from django.test import TestCase

from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie
movie = ia.get_movie('0133093')

print(movie['genres'])

# print the genres of the movie
print('Genres:')
for genre in movie['genres']:
    print(genre)
