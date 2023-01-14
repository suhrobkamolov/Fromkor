# books/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("", views.members, name="home"),
]










