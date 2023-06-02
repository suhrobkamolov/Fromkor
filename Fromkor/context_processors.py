from Movies.models import Movie, Genre, TVSeries
from mainhome.models import Profile, userStripe


def app_data(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all().order_by('title')
    tv_series = TVSeries.objects.all()
    user_profile = Profile.objects.all()
    user_stripe = userStripe.objects.all()

    return {
        'movies_context': movies,
        'genres_context': genres,
        'tv_series_context': tv_series,
        'user_profile_context': user_profile,
        'user_stripe_context': user_stripe
    }

