from django.shortcuts import render, get_object_or_404
from .models import Movie, DailyMovieViews, TVSeries, DailySeriesViews, Episode, DailySeriesEpisodeViews
from django.utils import timezone
from django.http import JsonResponse
from imdb import IMDb

# Create your views here.


def watch_movie(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    today = timezone.now().date()
    daily_views, created = DailyMovieViews.objects.get_or_create(movie=movie, date=today)
    daily_views.views += 1
    daily_views.save()
    movie.movie_view_count += 1
    movie.save()
    return render(request, 'moviedetailed.html', {'movie': movie})


def watch_series(request, series_slug):
    series = get_object_or_404(TVSeries, slug=series_slug)
    today = timezone.now().date()
    daily_views, created = DailySeriesViews.objects.get_or_create(tv_series=series, date=today)
    daily_views.views += 1
    daily_views.save()
    series.view_count += 1
    series.save()
    return render(request, 'seriessingle.html', {'series': series})


def watch_series_episode(request, series_slug, episode_slug):
    series = get_object_or_404(TVSeries, slug=series_slug)
    episode = get_object_or_404(Episode, tv_series=series, slug=episode_slug)
    today = timezone.now().date()
    daily_views, created = DailySeriesEpisodeViews.objects.get_or_create(episode=episode, date=today)
    daily_views.views += 1
    daily_views.save()
    episode.episode_view_count += 1
    episode.save()
    return render(request, 'moviedetailed.html', {'episode': episode})


def fetch_data_view(request, imdb_id):
    ia = IMDb()
    series = ia.get_movie(imdb_id)
    cast = series.get('cast')
    cast_list = [i.get('name') for i in cast]
    # convert genre strings to Genre model instances
    genres = [g for g in series.get('genres')]
    data = {
        'title': series.get('title', ''),
        'description': series.get('plot outline', ''),
        'release_year': series.get('series years'),
        'num_seasons': series.get('seasons'),
        'genres': genres,
        'poster_url': series.get('full-size cover url'),
        'rating': series.get('rating'),
        'cast': cast_list,
        'episodes': series.get('episodes'),
    }
    return JsonResponse(data)


def fetch_data_episode(request, imdb_id):
    ia = IMDb()
    episode = ia.get_movie(imdb_id)
    cast = episode.get('cast')
    cast_list = [i.get('name') for i in cast]
    director = episode.get('director')
    director_list = [i.get('name') for i in director]
    writer = episode.get('writer')
    writer_list = [i.get('name') for i in writer]
    producer = episode.get('producer')
    producer_list = [i.get('name') for i in producer]
    durations = episode.get('runtimes')
    duration = durations[0]
    " 'director', 'episode', 'episode title', 'full-size cover url', 'cast', "
    " 'original air date', 'producer', 'rating', 'runtimes', 'season', "
    "'title', 'writer', 'year'"
    data = {
        'title': episode.get('title', ''),
        'release_year': episode.get('series years'),
        'season': episode.get('season'),
        'episode_number': episode.get('episode'),
        'duration': duration,
        'description': episode.get('plot outline', ''),
        'rating': episode.get('rating'),
        'year': episode.get('year'),
        'original_air_date': episode.get('original air date'),
        'cast': cast_list,
        'director': director_list,
        'writer': writer_list,
        'producer': producer_list,
        'cover_url': episode.get('full-size cover url'),
    }
    return JsonResponse(data)

# class MoviesListView(ListView):
#     model = Movie
#
#
# class MoviesDetailView(DetailView):
#     model = Movie


# class WatchMovieView(View):
#     def get(self, request, movie_id):
#         movie = get_object_or_404(Movie, id=movie_id)
#         movie.movie_view_count += 1
#         movie.save()
#         # Render the movie detail template
#         return render(request, 'moviedetailed.html', {'movie': movie})


# class MostWatchedMoviesView(View):
#     def get(self, request):
#         movies = Movie.objects.all().order_by('-view_count')
#         return render(request, 'most_watched.html', {'movies': movies})





