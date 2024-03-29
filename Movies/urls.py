from django.urls import path
from .views import TVSeriesListView, watch_movie, watch_series, watch_series_episode, fetch_data_view, fetch_data_episode, MovieListView

urlpatterns = [
    path("movies/<slug:slug>/", watch_movie, name="Movie_Watch_View"),
    path("tv-series/<slug:series_slug>/", watch_series, name="Series_Watch_View"),
    path("tv-series/<slug:series_slug>/<slug:episode_slug>", watch_series_episode, name="Series_Episode_Watch_View"),
    path('fetch-data/<str:imdb_id>/', fetch_data_view, name='fetch_data'),
    path('fetch-data-ep/<str:imdb_id>/', fetch_data_episode, name='fetch_data_episode_view'),
    path('movie-list/', MovieListView.as_view(), name='movie_list'),
    path('tv-series-list/', TVSeriesListView.as_view(), name='tvseries_list'),
]
