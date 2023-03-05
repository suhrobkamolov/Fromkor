from django.shortcuts import render, get_object_or_404
# from django.views import View
# from django.views.generic import ListView, DetailView
from .models import Movie, DailyMovieViews, TVSeries, DailySeriesViews
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


def watch_series(request, slug):
    series = get_object_or_404(TVSeries, slug=slug)
    today = timezone.now().date()
    daily_views, created = DailySeriesViews.objects.get_or_create(tv_series=series, date=today)
    daily_views.views += 1
    daily_views.save()
    series.view_count += 1
    series.save()
    return render(request, 'moviedetailed.html', {'series': series})


def fetch_data_view(request, imdb_id):
    ia = IMDb()
    series = ia.get_movie(imdb_id)
    cast = series.get('cast')
    cast_list = [i.get('name') for i in cast]

    data = {
        'title': series.get('title', ''),
        'description': series.get('plot outline', ''),
        'release_year': series.get('series years'),
        'num_seasons': series.get('seasons'),
        'genres': series.get('genre'),
        'poster_url': series.get('full-size cover url'),
        'rating': series.get('rating'),
        'cast': cast_list,
        'episodes': series.get('episodes'),

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





