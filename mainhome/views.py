from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Sum
from Movies.models import Movie, Category, DailyMovieViews
from .models import Carousel


# def members(request):
#     template = loader.get_template('home.html')
#     return HttpResponse(template.render())


def home(request):
    period = 7  # the number of days to include in the view count
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=period)
    movie_views = DailyMovieViews.objects.filter(date__range=(start_date, end_date)) \
        .values('movie') \
        .annotate(views=Sum('views')) \
        .order_by('-views')
    most_watched_movies = [Movie.objects.get(id=view['movie']) for view in movie_views]
    carousel_objects = Carousel.objects.all()
    categoryset = Category.objects.all()
    queryset = Movie.objects.filter(created__gte=start_date)
    context = {
        'carousel_list': carousel_objects,
        'recent_movie_list': queryset,
        'category_list': categoryset,
        'movies': most_watched_movies
    }
    return render(request, 'home.html', context)


# Create your views here.
