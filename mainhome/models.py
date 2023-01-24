from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
from Movies.models import Movie


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
    title = models.CharField(max_length=140)
    to_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='d')

    def __str__(self):
        return self.title


class profile(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(default='description default text')

    def __str__(self):
        return self.name


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username


def my_callback(sender, **kwargs):
    print("request finished")
    print(kwargs)


user_logged_in.connect(my_callback)






