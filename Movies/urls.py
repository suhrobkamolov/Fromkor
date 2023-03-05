from django.urls import path
from .views import watch_movie, watch_series, fetch_data_view

urlpatterns = [
    path("<slug:slug>/", watch_movie, name="Movie_Watch_View"),
    path("<slug:slug>/", watch_series, name="Series_Watch_View"),
    path('fetch-data/<str:imdb_id>/', fetch_data_view, name='fetch_data'),
]

