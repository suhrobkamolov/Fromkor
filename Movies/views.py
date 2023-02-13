from django.shortcuts import render, get_object_or_404
# from django.views import View
# from django.views.generic import ListView, DetailView
from .models import Movie, DailyMovieViews
from django.utils import timezone

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





