from django.contrib import admin
from .models import Carousel, Profile, FavoriteMovie, FavoriteTVSeries

# Register your models here.


class CarouselClass(admin.ModelAdmin):
    list_display = ('title', 'to_movie')
    list_display_links = ('title',)
    list_per_page = 20
    ordering = ['title']
    search_fields = ['title', 'description']


admin.site.register(Carousel, CarouselClass)


class ProfileClass(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    list_per_page = 20
    ordering = ['user']
    search_fields = ['user', ]


admin.site.register(Profile, ProfileClass)
admin.site.register(FavoriteMovie)
admin.site.register(FavoriteTVSeries)




