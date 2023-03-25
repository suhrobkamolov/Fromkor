from django import template

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

