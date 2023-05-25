from django.core.management.base import BaseCommand
from Movies.models import WatchMovieUrl, Movie


class Command(BaseCommand):
    help = 'Add MovieWatchUrls'

    def handle(self, *args, **options):
        vidsrc_base_url = "https://vidsrc.me/embed/tt"

        existing_urls = WatchMovieUrl.objects.filter(channel='VIDSRC').values_list('movie__imdb_id', flat=True)

        movies_without_url = Movie.objects.exclude(imdb_id__in=existing_urls)

        for movie in movies_without_url:
            if movie.movie_imdb:
                imdb_id = movie.imdb_id
                url_to_be = f"{vidsrc_base_url}{imdb_id}"
                print(url_to_be)

                watch_url = WatchMovieUrl.objects.create(
                    url=url_to_be,
                    channel='VIDSRC',
                    movie=movie
                )


