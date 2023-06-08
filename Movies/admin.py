from django.contrib import admin
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Genre, Company, Producer, Actor, Movie, DailyMovieViews, TVSeries,\
    Episode, DailySeriesEpisodeViews, WatchMovieUrl, ActorRoleByMovie, ActorRoleByEpisode

from PIL import Image
import requests
from io import BytesIO
from django.core.files import File
from .forms import TVSeriesAdminForm

# Register your models here.


class TVSeriesAdmin(admin.ModelAdmin):
    model = TVSeries
    list_display = ['title', 'slug', 'release_date', 'created', 'updated',]
    list_filter = ['created', 'updated', 'genre']
    list_editable = ['release_date', ]
    list_per_page = 50
    ordering = ['-created']
    search_fields = ['title', 'description',]
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('detailed_picture_show',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(verbose_name='Genres', is_stacked=False)},
    }
    form = TVSeriesAdminForm

    def poster_url_change(self, obj):
        url = obj.poster_url
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((285, 437), Image.ANTIALIAS)
        filestream = BytesIO()
        image.save(filestream, 'JPEG')
        filestream.seek(0)
        obj.poster.save(obj.poster_url.split('/')[-1], File(filestream), save=False)

    def save_model(self, request, obj, form, change):
        if change:  # if editing an existing object
            old_obj = TVSeries.objects.get(pk=obj.pk)
            if 'poster' in form.changed_data:
                # if obj.poster != old_obj.poster:  # if poster field has changed
                #     # check if old_obj.poster exists, and prompt user to confirm overwriting
                #     if old_obj.poster:
                #         old_obj.poster.delete(save=False)
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                # if old_obj.poster:
                #     old_obj.poster.delete(save=False)
                self.poster_url_change(obj)
                super().save_model(request, obj, form, change)
        else:
            if obj.poster:
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                self.poster_url_change(obj)
                super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)  # continue with saving the object


admin.site.register(TVSeries, TVSeriesAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tv_series', 'season', 'episode_number', 'created', 'updated',)
    list_display_links = ('title',)
    list_per_page = 20
    ordering = ['tv_series', 'season', 'episode_number']
    list_filter = ['tv_series', 'created', 'updated']
    search_fields = ['title', 'description', ]
    exclude = ('created', 'updated',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if change:  # if editing an existing object
            old_obj = Episode.objects.get(pk=obj.pk)
            if 'cover' in form.changed_data:
                # old_obj.cover.delete(save=False)
                super().save_model(request, obj, form, change)
            elif obj.cover_url:
                # if old_obj.cover:
                #     old_obj.cover.delete(save=False)
                url = obj.cover_url
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                # image = image.resize((285, 437), Image.ANTIALIAS)
                filestream = BytesIO()
                image.save(filestream, 'JPEG')
                filestream.seek(0)
                obj.cover.save(obj.cover_url.split('/')[-1], File(filestream), save=False)
                super().save_model(request, obj, form, change)
        else:
            if obj.cover:
                super().save_model(request, obj, form, change)
            elif obj.cover_url:
                url = obj.cover_url
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                # image = image.resize((285, 437), Image.ANTIALIAS)
                filestream = BytesIO()
                image.save(filestream, 'JPEG')
                filestream.seek(0)
                obj.cover.save(obj.cover_url.split('/')[-1], File(filestream), save=False)
                super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)  # continue with saving the object


admin.site.register(Episode, EpisodeAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at',)
    list_display_links = ('title',)
    list_per_page = 20
    ordering = ['title']
    search_fields = ['title', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Genre, GenreAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'release_date', 'is_active']
    list_filter = ['created', 'updated', 'genre']
    list_editable = ['is_active', ]
    list_per_page = 50
    ordering = ['-created']
    search_fields = ['title', 'plot_summary']
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not change:
            # Creating a new movie object
            if not obj.poster and obj.poster_url:
                # No poster uploaded but poster_url is provided
                try:
                    response = requests.get(obj.poster_url)
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((285, 437), Image.ANTIALIAS)
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG')
                    obj.poster.save(f'{obj.title}.jpg', ContentFile(img_io.getvalue()), save=False)
                    obj.poster_url = ''
                except Exception as e:
                    print(f'Error downloading image: {e}')
            elif obj.poster:
                img = Image.open(obj.poster)
                img = img.resize((285, 437), Image.ANTIALIAS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                obj.poster.save(f'{obj.title}.jpg', ContentFile(img_io.getvalue()), save=False)
        else:
            old_obj = Movie.objects.get(pk=obj.pk)
            # Updating an existing movie object
            if 'poster' in form.changed_data and obj.poster != old_obj.poster:
                # New poster uploaded
                img = Image.open(form.cleaned_data['poster'])
                img = img.resize((285, 437), Image.ANTIALIAS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                obj.poster.save(f'{obj.title}.jpg', ContentFile(img_io.getvalue()), save=False)
            elif obj.poster_url:
                try:
                    response = requests.get(obj.poster_url)
                    img = Image.open(BytesIO(response.content))
                    img = img.resize((285, 437), Image.ANTIALIAS)
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG')
                    obj.poster.save(f'{obj.title}.jpg', ContentFile(img_io.getvalue()), save=False)
                    obj.poster_url = ''
                except Exception as e:
                    print(f'Error downloading image: {e}')
        super().save_model(request, obj, form, change)


class ActorAdmin(admin.ModelAdmin):
    list_display = ['actor_name', 'slug', 'imdb_id', 'is_active']
    list_filter = ['created_at', 'updated_at']
    list_editable = ['is_active', ]
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['actor_name', 'imdb_id', ]
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('actor_name',)}


admin.site.register(Movie, MovieAdmin)

admin.site.register(Company)
admin.site.register(Producer)
admin.site.register(Actor, ActorAdmin)
admin.site.register(DailyMovieViews)
admin.site.register(DailySeriesEpisodeViews)
admin.site.register(WatchMovieUrl)
admin.site.register(ActorRoleByMovie)
admin.site.register(ActorRoleByEpisode)






