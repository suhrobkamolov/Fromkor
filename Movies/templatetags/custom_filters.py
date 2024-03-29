from django import template
import datetime

register = template.Library()


@register.filter
def latest_episode_cover_url(tv_series):
    latest_episode = tv_series.episodes.latest("episode_number")
    return latest_episode.cover.url


@register.filter
def latest_episode_season(tv_series):
    latest_episode = tv_series.episodes.latest("episode_number")
    return latest_episode.season


@register.filter
def season_episode_count(tv_series):
    latest_episode = tv_series.episodes.latest("episode_number")
    x = 0
    for i in tv_series.episodes.all():
        if i.season == latest_episode.season:
            x += 1
    return x


@register.filter
def season_episode_air_date(tv_series):
    latest_episode = tv_series.episodes.latest("episode_number")
    for i in tv_series.episodes.all():
        if i.season == latest_episode.season and i.episode_number == 1:
            return i.original_air_date


@register.filter
def series_total_run_time(tv_series):
    total_runtime = datetime.timedelta()
    for i in tv_series.episodes.all():
        total_runtime += i.duration
    total_minutes = int(total_runtime.total_seconds() / 60)
    if total_minutes > 60:
        return str(total_minutes//60)+'h '+str(total_minutes % 60)+'m'
    else:
        return str(total_minutes)+'m'


@register.simple_tag(takes_context=True)
def get_filter_url(context, view):
    request = context['request']
    params = request.GET.copy()

    # Remove existing 'view' parameter
    if 'view' in params:
        del params['view']

    # Set the 'view' parameter to the desired value
    params['view'] = view

    return f"?{params.urlencode()}"




