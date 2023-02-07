from django.urls import path
from .views import watch_movie
urlpatterns = [
    path("<slug:slug>/", watch_movie, name="Movie_Watch_View"),
]

