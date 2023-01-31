from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from Movies.models import Movie, Category
from .models import Carousel


# def members(request):
#     template = loader.get_template('home.html')
#     return HttpResponse(template.render())


def home(request):
    carousel_objects = Carousel.objects.all()
    categoryset = Category.objects.all()
    queryset = Movie.objects.all()
    context = {
        'carousel_list': carousel_objects,
        'object_list': queryset,
        'category_list': categoryset,
    }
    return render(request, 'home.html', context)

# Create your views here.
