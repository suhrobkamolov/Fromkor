from Movies.models import Movie, Genre, TVSeries


def app_data(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all().order_by('title')
    tv_series = TVSeries.objects.all()

    return {
        'movies_context': movies,
        'genres_context': genres,
        'tv_series_context': tv_series,
    }

