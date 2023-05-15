from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import Movie, Genre, DailyMovieViews, TVSeries, DailySeriesViews, Episode, DailySeriesEpisodeViews, WatchMovieUrl
from django.utils import timezone
from django.http import JsonResponse
from imdb import IMDb
from django.core.paginator import Paginator
import nltk
from nltk.corpus import stopwords
from django.urls import reverse_lazy

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))


def watch_movie(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    cast = movie.cast.all()
    today = timezone.now().date()
    daily_views, created = DailyMovieViews.objects.get_or_create(movie=movie, date=today)
    daily_views.views += 1
    daily_views.save()
    movie.movie_view_count += 1
    movie.save()
    if movie.imdb_id and len(cast) < 15:
        ia = IMDb()
        movie_from_imdb = ia.get_movie(movie.imdb_id)
        cast = movie_from_imdb.get("cast")
    movie_urls = WatchMovieUrl.objects.filter(movie=movie)
    return render(request, 'moviedetailed.html', {'movie': movie, 'cast': cast, "movie_urls": movie_urls}, )


def watch_series(request, series_slug):
    series = get_object_or_404(TVSeries, slug=series_slug)
    cast = series.cast.all()
    episodes = series.episodes.all()
    season_list = []            # cast_list.append({"name": name, "image_url": image_url})
    for s in range(series.num_seasons):
        season_episodes = series.episodes.filter(season=s+1).order_by("episode_number")
        if episodes.filter(season=s+1).count() > 0:
            season_list.append({'season_number': s+1, "total_episode": episodes.filter(season=s+1).count(),
                                "air_date": episodes.filter(season=s+1).get(episode_number=1).original_air_date,
                                "cover_url": episodes.filter(season=s+1).get(episode_number=1).cover.url,
                                "season_episodes": season_episodes})

    if series.imdb_id and len(cast) < 15:
        ia = IMDb()
        movie = ia.get_movie(series.imdb_id)
        cast = movie.get("cast")

    today = timezone.now().date()
    daily_views, created = DailySeriesViews.objects.get_or_create(tv_series=series, date=today)
    daily_views.views += 1
    daily_views.save()
    series.view_count += 1
    series.save()
    return render(request, 'seriessingle.html', {'series': series, 'cast': cast,
                                                 'episodes': episodes, 'season_list': season_list})


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
    # cast = series.get('cast')
    # cast_list = [i.get('name') for i in cast]
    # # convert genre strings to Genre model instances
    # genres = [g for g in series.get('genres')]
    data = {
        'title': series.get('title', ''),
        'release_date': series.get('original air date'),
        'year': series.get('year'),
        'description': series.get('plot outline', ''),
        'run_time': series.get('runtimes')[0],
        'rating': series.get('rating'),
        'votes': series.get('votes'),
        'poster_url': series.get('full-size cover url'),
        'release_year': series.get('series years'),
        'num_seasons': series.get('seasons'),
        'episodes': series.get('episodes'),
        # 'cast': cast_list,
        # 'genres': genres,
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


class MovieListView(ListView):
    model = Movie
    template_name = 'moviegrid.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()

        # filter by name
        search_query = self.request.GET.get('name')
        # if name:
        #     queryset = queryset.filter(title__icontains=name)
        if search_query:
            # Tokenize search query and remove stopwords
            tokens = nltk.word_tokenize(search_query.lower())
            tokens = [token for token in tokens if token not in STOPWORDS]
            # Construct Q objects to search for similar titles and descriptions
            title_q = Q(title__icontains=search_query)
            desc_q = Q()
            for token in tokens:
                desc_q &= Q(plot_summary__icontains=token)
            # Combine title and description queries using OR
            queryset = queryset.filter(title_q | desc_q)

        # filter by genre
        genres = self.request.GET.getlist('genres')
        if genres:
            queryset = queryset.filter(genre__id__in=genres).distinct()

        # sort by rating
        rating = self.request.GET.get('rating')
        if rating:
            if rating == '5':
                queryset = queryset.filter(movie_imdb__gte=5)
            elif rating == '6':
                queryset = queryset.filter(movie_imdb__gte=6)
            elif rating == '7':
                queryset = queryset.filter(movie_imdb__gte=7)
            elif rating == '8':
                queryset = queryset.filter(movie_imdb__gte=8)
            elif rating == '9':
                queryset = queryset.filter(movie_imdb__gte=9)

        year_f = self.request.GET.get('year-from')
        year_t = self.request.GET.get('year-to')
        if year_f:
            queryset = queryset.filter(year__gte=year_f)
        if year_t:
            queryset = queryset.filter(year__lte=year_t)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_size = int(self.request.GET.get('page_size', 12))
        self.paginate_by = page_size  # Update the pagination property
        movies = self.get_queryset()
        paginator = Paginator(movies, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['movies'] = page_obj
        context['paginator'] = page_obj.paginator
        context['page_obj'] = page_obj
        context['page_sizes'] = [10, 20]  # Add available page sizes to the context
        context['movies_per_page'] = page_size

        # add search and filter values to context
        context['search_name'] = self.request.GET.get('name', '')
        context['filter_genre'] = self.request.GET.getlist('genres', '')
        context['filter_rating'] = self.request.GET.get('rating', '')
        context['year_from'] = self.request.GET.get('year-from', '')
        context['year_to'] = self.request.GET.get('year-to', '')

        # get all available genres
        context['genres'] = Genre.objects.all().order_by('title')
        # context['load_more_url'] = reverse_lazy('load_more_movies')

        return context

    def get_paginate_by(self, queryset):
        """
        Return the number of items to paginate by based on the GET parameters.
        """
        page_size = self.request.GET.get('page_size', 10)
        return int(page_size)



