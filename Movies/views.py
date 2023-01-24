from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Movie

# Create your views here.


class MoviesListView(ListView):
    model = Movie


class MoviesDetailView(DetailView):
    model = Movie






