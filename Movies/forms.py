from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import TVSeries

from django.forms.widgets import ClearableFileInput
from django.utils.html import mark_safe


class ImageWidget(ClearableFileInput):
    template_with_initial = '<p class="file-upload">%s</p>'
    template_with_clear = '<label for="%s">%s</label> <input type="checkbox" name="%s-clear" id="%s-clear_id"> <label for="%s-clear_id" class="file-clear">%s</label>'
    template_with_no_input = '<span>%s</span>'

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs)
        if value and hasattr(value, "url"):
            html += f'<img src="{value.url}" width="142" height="218" />'
        return mark_safe(html)


class TVSeriesAdminForm(forms.ModelForm):
    poster = forms.ImageField(widget=ImageWidget)

    class Meta:
        model = TVSeries
        fields = ['imdb_id', 'title', 'slug', 'release_date', 'release_year', 'num_seasons', 'description', 'genre',
                  'trailer', 'rating', 'cast', 'director', 'writers', 'producer', 'episodes', 'MPAA_rating', 'view_count', 'is_active',
                  'fetch_data', 'is_continuing', 'poster', 'poster_url']

    def clean(self):
        cleaned_data = super().clean()
        poster = cleaned_data.get('poster')
        poster_url = cleaned_data.get('poster_url')

        if not poster and not poster_url:
            raise ValidationError({
                'poster': _('Either poster or poster_url must be provided.'),
                'poster_url': _('Either poster or poster_url must be provided.'),
            })

        return cleaned_data

