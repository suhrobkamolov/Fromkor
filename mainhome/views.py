from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Sum
from Movies.models import Movie, Genre, DailyMovieViews, DailySeriesEpisodeViews, TVSeries, Episode
from .models import Carousel
from itertools import chain


# def members(request):
#     template = loader.get_template('home.html')
#     return HttpResponse(template.render())


def home(request):
    period = 90 # the number of days to include in the view count
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=period)
    movie_views = DailyMovieViews.objects.filter(date__range=(start_date, end_date)) \
        .values('movie') \
        .annotate(views=Sum('views')) \
        .order_by('-views')
    episode_views = DailySeriesEpisodeViews.objects.filter(date__range=(start_date, end_date)) \
        .values('episode') \
        .annotate(views=Sum('views')) \
        .order_by('-views')
    most_watched_movies = [Movie.objects.get(id=view['movie']) for view in movie_views]
    most_watched_episodes = [Episode.objects.get(id=view['episode']) for view in episode_views]
    combined_views = sorted(chain(movie_views, episode_views), key=lambda x: x['views'], reverse=True)
    most_watched_items = []
    for view in combined_views:
        if 'movie' in view:
            most_watched_items.append(Movie.objects.get(id=view['movie']))
        elif 'episode' in view:
            most_watched_items.append(Episode.objects.get(id=view['episode']))
    carousel_objects = Carousel.objects.all()
    categoryset = Genre.objects.order_by('title')
    queryset = Movie.objects.filter(created__gte=start_date)
    latest_episodes = Episode.objects.filter(created__gte=start_date)
    context = {
        'carousel_list': carousel_objects,
        'recent_movie_list': queryset,
        'category_list': categoryset,
        'movies': most_watched_movies,
        'episodes': most_watched_episodes,
        "mostwatcheditems": most_watched_items,
        "latest_episodes": latest_episodes
    }
    return render(request, 'home.html', context)


# Create your views here.
