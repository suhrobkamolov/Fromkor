from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator

from Movies.models import Movie, TVSeries
from django.contrib.auth.models import AbstractUser, Group, Permission

STATUS_CHOICES = (
    ('M1', 'Movie1'),
    ('M2', 'Movie2'),
    ('M3', 'Movie3'),
    ('M4', 'Movie4'),
    ('M5', 'Movie5'),
    ('M6', 'Movie6'),
    ('d', 'Draft'),
)


class Carousel(models.Model):
    title = models.CharField(max_length=140, null=True, blank=True)
    to_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='CarouselItemMovies',
                                 null=True, blank=True)
    to_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='CarouselItemTVSeries',
                                  null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='d', unique=True)

    def __str__(self):
        return f"{self.title}, ({self.status})"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='user_profile')

    def upload_file_name(self, filename):
        x = self.user.username
        characters_to_remove = '<,>,:,",/,\,|,?,*,.'
        for character in characters_to_remove:
            x = x.replace(character, "")
        return f'users/{x}/images/{filename}'

    country = CountryField(blank_label="(select country)", multiple=False, blank=True, null=True)
    profile_favorite_movies = models.ManyToManyField(Movie, through='FavoriteMovie', blank=True, related_name='user_favorite_movies')
    favorite_tvseries = models.ManyToManyField(TVSeries, through='FavoriteTVSeries', blank=True, related_name="users_favorite_tvseries")
    avatar = models.ImageField(upload_to=upload_file_name, blank=True, null=True)

    def __str__(self):
        return self.user.username


class FavoriteMovie(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorite_movies_relation')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_favorites')

    def __str__(self):
        return f"{self.user_profile.user.username}: {self.movie.title}"


class FavoriteTVSeries(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorite_tvseries_relation')
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='user_favorites')

    def __str__(self):
        return f"{self.user_profile.user.username}: {self.tv_series.title}"


class UserMovieRate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_rate')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_movie_rate')
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='user_tv_series_rate', null=True, blank=True)
    movie_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    tv_series_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.movie}: {self.movie_rating} | {self.tv_series}: {self.tv_series_rating})"


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_stripe')
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username


# def my_callback(sender, **kwargs):
#     print("request finished")
#     print(kwargs)
#
#
# user_logged_in.connect(my_callback)






