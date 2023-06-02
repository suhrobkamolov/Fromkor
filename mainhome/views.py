from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta, date
from django.views.generic import ListView
from django.db.models import Sum
from itertools import chain
from django.db.models import Q
import nltk
from nltk.corpus import stopwords
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from Movies.models import Movie, Genre, DailyMovieViews, DailySeriesEpisodeViews, TVSeries, Episode
from .models import Carousel, Profile, FavoriteMovie
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django_countries import countries
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST


nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))


def handler404(request, exception):
    return render(request, '404.html', status=404)


def home(request):
    user = request.user
    period = 90  # the number of days to include in the view count
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
    favorite_movies = []
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        favorite_movies = FavoriteMovie.objects.filter(user_profile=user_profile).values_list('movie_id', flat=True)
    context = {
        'carousel_list': carousel_objects,
        'recent_movie_list': queryset,
        'category_list': categoryset,
        'movies': most_watched_movies,
        'episodes': most_watched_episodes,
        "mostwatcheditems": most_watched_items,
        "latest_episodes": latest_episodes,
        "favorite_movies": favorite_movies,
    }
    return render(request, 'home.html', context)


class SearchResultsView(ListView):
    template_name = 'searchresult.html'
    context_object_name = 'movies'

    def get_queryset(self):
        movies = Movie.objects.all()
        series = TVSeries.objects.all()
        search_query = self.request.GET.get('search')
        search_option = self.request.GET.get("search-for")
        queryset = Movie.objects.none()  # Empty initial queryset

        if search_option == "movies":
            if search_query:
                tokens = nltk.word_tokenize(search_query.lower())
                tokens = [token for token in tokens if token not in STOPWORDS]
                title_q = Q(title__icontains=search_query)
                desc_q = Q()
                for token in tokens:
                    desc_q &= Q(plot_summary__icontains=token)
                # Combine title and description queries using OR
                queryset = movies.filter(title_q | desc_q)
        elif search_option == "tv-series":
            if search_query:
                tokens = nltk.word_tokenize(search_query.lower())
                tokens = [token for token in tokens if token not in STOPWORDS]
                title_q = Q(title__icontains=search_query)
                desc_q = Q()
                for token in tokens:
                    desc_q &= Q(description__icontains=token)
                queryset = series.filter(title_q | desc_q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pagination
        page_size = int(self.request.GET.get('page_size', 12))
        self.paginate_by = page_size  # Update the pagination property
        movies = self.get_queryset()
        paginator = Paginator(movies, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['movies'] = page_obj
        context['paginator'] = page_obj.paginator
        context['page_obj'] = page_obj
        context['movies_per_page'] = page_size

        view_mode = self.request.GET.get('view', 'grid')
        # Set a flag based on the selected view mode
        grid_view = view_mode == 'grid'
        list_view = view_mode == 'list'
        context['grid_view'] = grid_view
        context['list_view'] = list_view

        search_query = self.request.GET.get('search')
        search_option = self.request.GET.get("search-for")

        # Preserve the search query and search option in the context
        context['search_query'] = search_query
        context['search_option'] = search_option

        return context


class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Check if user is already signed in
            return redirect('home')  # Redirect to the desired page

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['next_url'] = self.request.GET.get('next', '/')
        return response


@login_required
def profile(request):
    user = request.user  # Get the currently logged-in user
    user_profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': user_profile,
    }
    return render(request, 'userprofile.html', context)


@login_required
def update_profile(request):
    user = request.user  # Get the currently logged-in user
    user_profile = Profile.objects.get(user=user)
    choices = [(code, name) for code, name in countries]
    error_messages = {
        "username_taken": "Username is already taken!",
        "first_name": "First Name and Last Name field is required!",
    }
    errors = []
    context = {
        'user_profile': user_profile,
        'country_choices': choices,
        'errors': errors,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        avatar = request.FILES.get('avatar')  # Use request.FILES to retrieve the uploaded file

        if user.username != username and User.objects.filter(username=username).exists():
            errors.append(error_messages["username_taken"])
            return render(request, 'userprofile_change.html', context)
        elif not first_name or not last_name:
            errors.append(error_messages["first_name"])
            return render(request, 'userprofile_change.html', context)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if avatar:
            user_profile.avatar = avatar
        user_profile.country = request.POST.get('country')
        user_profile.save()

        return redirect('update_profile')

    return render(request, 'userprofile_change.html', context)


@login_required
def remove_avatar(request):
    if request.method == 'POST':
        profile = request.user.user_profile
        if profile.avatar:
            profile.avatar.delete()  # Remove the avatar file
            profile.avatar = None  # Clear the avatar field in the model
            profile.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Avatar does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@require_POST
@login_required
def add_to_favorite(request):
    movie_id = request.POST.get('movie_id')
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    user_profile = Profile.objects.get(user=user)
    favorite_movie, created = FavoriteMovie.objects.get_or_create(user_profile=user_profile, movie=movie)

    if created:
        added = True
    else:
        favorite_movie.delete()
        added = False

    return JsonResponse({'added': added})


class UserFavoriteMovies(LoginRequiredMixin, ListView):
    model = FavoriteMovie
    template_name = "userfavoritegrid.html"
    context_object_name = 'movies'
    paginate_by = 24

    def get_queryset(self):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        queryset = FavoriteMovie.objects.filter(user_profile=user_profile).select_related('movie')
        sort_by = self.request.GET.get('sort-by')
        if sort_by:
            if sort_by == 'recommended':
                queryset = queryset
            elif sort_by == 'rating-d':
                queryset = queryset.order_by('-movie__movie_imdb')
            elif sort_by == 'rating-a':
                queryset = queryset.order_by('movie__movie_imdb')
            elif sort_by == 'latest-d':
                queryset = queryset.order_by('-movie__created')
            elif sort_by == 'latest-a':
                queryset = queryset.order_by('movie__created')
            elif sort_by == 'year-d':
                queryset = queryset.order_by('-movie__year')
            elif sort_by == 'year-a':
                queryset = queryset.order_by('movie__year')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies_per_page'] = self.paginate_by
        context['sort_by'] = self.request.GET.get('sort-by', '')
        return context






