from django.contrib import admin
from .models import Carousel

# Register your models here.


class CarouselClass(admin.ModelAdmin):
    list_display = ('title', 'to_movie')
    list_display_links = ('title',)
    list_per_page = 20
    ordering = ['title']
    search_fields = ['title', 'description']


admin.site.register(Carousel, CarouselClass)




