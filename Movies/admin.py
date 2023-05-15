from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Genre, Company, Producer, Actor, Movie, DailyMovieViews, TVSeries,\
    Episode, DailySeriesEpisodeViews, WatchMovieUrl

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
                if obj.poster != old_obj.poster:  # if poster field has changed
                    # check if old_obj.poster exists, and prompt user to confirm overwriting
                    if old_obj.poster:
                        old_obj.poster.delete(save=False)
                        # response = input("Are you sure you want to change the existing poster image? (y/n): ")
                        # if response.lower() != 'y':
                        #     raise ValidationError('Cancelled. The poster image has not been changed.')
                    # elif obj.poster and not old_obj.poster:
                    #     super().save_model(request, obj, form, change)
                    # else:
                    #     if obj.poster_url:
                    #         self.poster_url_change(obj)
                    #     elif not obj.pk:
                    #         super().save_model(request, obj, form, change)
                    #     super().save_model(request, obj, form, change)
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                if old_obj.poster:
                    old_obj.poster.delete(save=False)
                self.poster_url_change(obj)
                super().save_model(request, obj, form, change)
        else:
            if obj.poster:
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                self.poster_url_change(obj)
                super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)  # continue with saving the object

    # def get_changeform_initial_data(self, request):
    #     initial = super().get_changeform_initial_data(request)
    #     initial['fetch_data'] = False
    #     return initial


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
                old_obj.cover.delete(save=False)
                super().save_model(request, obj, form, change)
            elif obj.cover_url:
                if old_obj.cover:
                    old_obj.cover.delete(save=False)
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
    list_display = ['title', 'slug', 'release_date', "is_active"]
    list_filter = ['created', 'updated', 'genre']
    list_editable = ['is_active', ]
    list_per_page = 50
    ordering = ['-created']
    search_fields = ['title', 'plot_summary', ]
    exclude = ('created_at', 'updated_at',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:  # if editing an existing object
            old_obj = Movie.objects.get(pk=obj.pk)
            if obj.poster:
                old_obj.poster.delete(save=False)
                image = Image.open(obj.poster.path)
                image = image.resize((285, 437), Image.ANTIALIAS)
                image.save(obj.poster.path)
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                old_obj.poster.delete(save=False)
                url = obj.poster_url
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                image = image.resize((285, 437), Image.ANTIALIAS)
                filestream = BytesIO()
                image.save(filestream, 'JPEG')
                filestream.seek(0)
                obj.poster.save(obj.poster_url.split('/')[-1], File(filestream), save=False)
                super().save_model(request, obj, form, change)
        else:
            if obj.poster:
                image = Image.open(obj.poster.path)
                image = image.resize((285, 437), Image.ANTIALIAS)
                image.save(obj.poster.path)
                super().save_model(request, obj, form, change)
            elif obj.poster_url:
                url = obj.poster_url
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
                image = image.resize((285, 437), Image.ANTIALIAS)
                filestream = BytesIO()
                image.save(filestream, 'JPEG')
                filestream.seek(0)
                obj.poster.save(obj.poster_url.split('/')[-1], File(filestream), save=False)
                super().save_model(request, obj, form, change)


admin.site.register(Movie, MovieAdmin)

admin.site.register(Company)
admin.site.register(Producer)
admin.site.register(Actor)
admin.site.register(DailyMovieViews)
admin.site.register(DailySeriesEpisodeViews)
admin.site.register(WatchMovieUrl)

# <iframe src="https://vk.com/video_ext.php?oid=202234924&id=456239899&hash=5d3f6b8743fe71f3" width="640" height="360" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>
# <iframe src="https://vk.com/video_ext.php?oid=-67429811&id=456242476&hash=f6debdff836c10c8" width="640" height="360" frameborder="0" allowfullscreen="1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture"></iframe>



