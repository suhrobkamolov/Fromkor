from django.contrib import admin
from .models import Category, Company, Producer, Actor, Movie, DailyMovieViews

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at',)
    list_display_links = ('title',)
    list_per_page = 20
    ordering = ['title']
    search_fields = ['title', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'slug', 'movie_release_date', 'created', 'updated']
    list_filter = ['created', 'updated', 'movie_genre']
    list_editable = ['movie_release_date', ]
    list_per_page = 50
    ordering = ['-created']
    search_fields = ['movie_title', 'movie_description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('movie_title',)}


admin.site.register(Movie, MovieAdmin)
admin.site.register(Company)
admin.site.register(Producer)
admin.site.register(Actor)
admin.site.register(DailyMovieViews)







