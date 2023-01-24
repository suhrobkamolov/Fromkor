from django.urls import path
from .views import MoviesListView, MoviesDetailView
urlpatterns = [
    path("", MoviesListView.as_view(), name="Movie List"),
    path("<int:pk>", MoviesDetailView.as_view(), name="Movie Detailed View"),
]
