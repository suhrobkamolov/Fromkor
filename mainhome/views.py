from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from Movies.models import Movie, Category


# def members(request):
#     template = loader.get_template('home.html')
#     return HttpResponse(template.render())


def home(request):
    categoryset = Category.objects.all()
    queryset = Movie.objects.all()
    context = {
        'object_list': queryset,
        'category_list': categoryset,
    }
    return render(request, 'home.html', context)

# Create your views here.
