from django.core.management.base import BaseCommand
from imdb import IMDb
from Movies.models import Movie, Genre, Company, Producer, Actor, ActorRoleByMovie
from django.utils.text import slugify
import re
import datetime
from django.db.utils import IntegrityError
from PIL import Image
import requests
from io import BytesIO
from django.core.files import File


MPAA_CHOICES = (
    ('G', 'General Audiences'),
    ('PG', 'Parental Guidance Suggested'),
    ('PG-13', 'Parents Strongly Cautioned'),
    ('R', 'Restricted'),
    ('NC-17', 'No Children 17 and Under Admitted'),
)
MPAA_s = ['G', 'PG', 'PG-13', 'R', 'NC-17']


def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9]', ' ', title).lower()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    slug = slugify(slug)
    return slug


def person(person_list):
    persons = []
    for data in person_list:
        try:
            producer_slug = data['name']
            imdb_id = data.getID()
            producer_name = data['name']
            producer_birthdate = datetime.datetime.today()
            person_tbc, _ = Producer.objects.get_or_create(
                producer_slug=generate_slug(producer_slug),
                defaults={
                    'imdb_id': imdb_id,
                    'producer_name': producer_name,
                    'producer_birthdate': producer_birthdate,
                    'producer_description': producer_name,
                }
            )
            persons.append(person_tbc)
        except KeyError:
            pass
    return persons


def actor(actor_list):
    actors = []
    for data in actor_list:
        try:
            person_tbc, _ = Actor.objects.get_or_create(
                slug=generate_slug(data['name']),
                defaults={
                    'imdb_id': data.getID(),
                    'actor_name': data['name'],
                    'actor_birthdate': datetime.datetime.today(),
                    'actor_mini_biography': data['name'],
                }
            )
            actors.append(person_tbc)

        except KeyError:
            pass
    return actors


class Command(BaseCommand):
    help = 'Add movies'

    def add_arguments(self, parser):
        parser.add_argument('imdb_ids', nargs='+', type=str, help='IMDb IDs of the movies')

    def handle(self, *args, **options):
        ia = IMDb()

        for imdb_id in options['imdb_ids']:
            # Fetch movie details from IMDb
            movie_data = ia.get_movie(imdb_id)
            # Extract relevant information
            title = movie_data['title']
            release_date = movie_data.get('original air date')
            year = movie_data.get('year')
            description = movie_data.get('plot outline', '')
            run_time = movie_data.get('runtimes')
            rating = movie_data.get('rating')
            votes = movie_data.get('votes')
            poster_url = movie_data.get('full-size cover url')

            genre_list = movie_data['genre']
            company_list = movie_data['production companies']
            producer_list = movie_data['producer']
            writer_list = movie_data['writer']
            director_list = movie_data['director']
            actor_list = movie_data['cast']

            slug_field = generate_slug(title)
            try:
                mpaa_rating = [i for i in [c.split(':')[1] for c in movie_data.get('certificates') if 'United States' in c] if i in MPAA_s][0]
            except:
                mpaa_rating = 'G'
            mpaa_choice = next((choice for choice in MPAA_CHOICES if choice[0] == mpaa_rating), None)

            # Create or update Genre instances
            genres = []
            for genre_name in genre_list:
                genre_slug = generate_slug(genre_name)
                try:
                    genre = Genre.objects.create(
                        title=genre_name,
                        slug=genre_slug,
                        description=genre_name,
                        meta_keywords=genre_name,
                        meta_description=genre_name,
                    )
                except IntegrityError:
                    # Genre with the same slug already exists, retrieve it instead
                    genre = Genre.objects.get(slug=genre_slug)
                genres.append(genre)
            # Create or update Company instances
            companies = []
            for company_data in company_list:
                company_slug = generate_slug(company_data['name'])
                company, _ = Company.objects.get_or_create(
                    company_name=company_data['name'],
                    defaults={
                        'company_slug': company_slug,
                        'company_description': company_data['name'],
                    }
                )
                companies.append(company)

            # Create or update Producer instances
            producer_list_obj = person(producer_list)
            director_list_obj = person(director_list)
            writer_list_obj = person(writer_list)
            actor_list_obj = actor(actor_list)

            # Create Movie instance
            movie, _ = Movie.objects.get_or_create(
                imdb_id=imdb_id,
                defaults={
                    'title': title,
                    'slug': slug_field,
                    'release_date': release_date,
                    'year': year,
                    'plot_summary': description,
                    'run_time': run_time,
                    'movie_imdb': rating,
                    'votes': votes,
                    'poster_url': poster_url,
                    'MPAA_rating': mpaa_choice[0] if mpaa_choice else MPAA_CHOICES[0],
                    # Set other movie fields accordingly
                }
            )

            # Set many-to-many relationships
            movie.genre.set(genres)
            movie.director.set(director_list_obj)
            movie.producer.set(producer_list_obj)
            movie.writer.set(writer_list_obj)
            movie.company.set(companies)
            movie.cast.set(actor_list_obj)
            print('Added Movie:', title)

            if poster_url:
                try:
                    response = requests.get(poster_url)
                    response.raise_for_status()
                    image = Image.open(BytesIO(response.content))
                    image = image.resize((285, 437), Image.ANTIALIAS)
                    filestream = BytesIO()
                    image.save(filestream, 'JPEG')
                    filestream.seek(0)
                    movie.poster.save(f'{movie.id}.jpg', File(filestream), save=True)
                except (requests.exceptions.RequestException, IOError) as e:
                    print(f"Failed to save movie poster: {str(e)}")

            actor_roles = movie_data.get('cast')

            # Create ActorRoleByMovie instances
            for actor_role_data in actor_roles:
                actor_name = actor_role_data['name']
                role = actor_role_data.currentRole
                try:
                    actor_obj = Actor.objects.get(actor_name=actor_name)
                    actor_role, _ = ActorRoleByMovie.objects.get_or_create(
                        actor=actor_obj,
                        movie=movie,
                        defaults={'role': role}
                    )
                except Actor.DoesNotExist:
                    print(f"Actor '{actor_name}' does not exist.")







