from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from PIL import Image
from django.utils.safestring import mark_safe


# Create your models here.

STATUS_CHOICES = (
    ('EN', 'English'),
    ('TR', 'Türkçe'),
    ('TJ', 'Tajik'),
    ('RU', 'Russian'),
)

# MOVIE_STATUS = (
#     ('RA', 'Recently Added'),
#     ('MW', 'Most Watched'),
#     ('TR', 'Top Rated'),
# )

MPAA = (
    ('G', 'General Audiences'),
    ('PG', 'Parental Guidance Suggested'),
    ('PG13', 'Parents Strongly Cautioned'),
    ('R', 'Restricted'),
    ('NC17', 'No Children 17 and Under Admitted'),
)


class Genre(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie:movie_list_by_genres', args=[self.slug])


class Company(models.Model):
    company_name = models.CharField(max_length=140)
    company_slug = models.SlugField(max_length=200, db_index=True, unique=True)
    company_description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return reverse('movie:movie_list_by_company', args=[self.company_slug])

# Producer model


class Producer(models.Model):
    producer_name = models.CharField(max_length=140)
    producer_surname = models.CharField(max_length=140)
    producer_birthdate = models.DateField()
    producer_death_date = models.DateField()
    producer_slug = models.SlugField(max_length=200, db_index=True, unique=True)
    producer_description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)
    was_actor = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Producer'
        verbose_name_plural = 'Producers'

    def __str__(self):
        return self.producer_name

    def get_absolute_url(self):
        return reverse('producer:product_list_by_producer', args=[self.producer_slug])

# Actor model


class Actor(models.Model):
    actor_name = models.CharField(max_length=140)
    actor_surname = models.CharField(max_length=140)
    actor_birthdate = models.DateField(max_length=140)
    actor_slug = models.SlugField(max_length=200, db_index=True, unique=True)
    actor_description = models.TextField()
    meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_producer = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return self.actor_name

    def get_absolute_url(self):
        return reverse('movies:movies_list_by_actor', args=[self.actor_slug])


class Movie(models.Model):

    def upload_file_name(self, filename):
        x = self.movie_title
        characters_to_remove = '<,>,:,",/,\,|,?,*,.'
        for character in characters_to_remove:
            x = x.replace(character, "")
        return f'movies/{x}/images/{filename}'

    slug = models.SlugField(unique=True)
    movie_title = models.CharField(max_length=120)
    movie_year = models.PositiveIntegerField(default=2023,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
        help_text="Use the following format: <YYYY>")
    movie_release_date = models.DateField()
    movie_duration = models.CharField(max_length=50, help_text='1h 20m')
    movie_MPAA_rating = models.CharField(choices=MPAA, max_length=4, default='G')
    movie_genre = models.ManyToManyField(Genre, default='UNDEFINED')
    movie_imdb = models.FloatField(default=5.0)
    movie_producer = models.ManyToManyField(Producer, default='UNDEFINED')
    movie_company = models.ManyToManyField(Company, default='UNDEFINED')
    movie_topic = models.CharField(max_length=120)
    movie_language = models.CharField(choices=STATUS_CHOICES, default=":)", max_length=120)
    movie_actors = models.ManyToManyField(Actor, default='/N')
    movie_image = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    thumb_url = models.CharField(max_length=500, null=True, blank=True)
    thumb = models.FileField(upload_to='movies/images', null=True, blank=True)
    movie_trailer_url = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    movie_status = models.CharField(max_length=120, null=True, blank=True)
    movie_view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    fetch_data = models.BooleanField(default=False)
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.movie_title

    def get_absolute_url(self):
        return reverse('Movie_Watch_View', args=[str(self.slug)])

    # Changing Movie image size before upload
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.movie_image.path)
        image = image.resize((285, 437), Image.ANTIALIAS)
        image.save(self.movie_image.path)


class DailyMovieViews(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    product = models.ForeignKey(Movie, on_delete=models.CASCADE)


def create_slug(instance, new_slag=None):
    slug = slugify(instance.name)
    if new_slag is not None:
        slug = new_slag
    qs = Movie.objects.filter(slug=slug).order_by('-id')
    exist = qs.exists()
    if exist:
        new_slag = '%s-%s' %(slug, qs.first().id)
        return create_slug(instance, new_slag=new_slag)
    return slug


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_slug, sender=Movie)

############# TV Series ######################


class TVSeries(models.Model):
    def upload_file_name(self, filename):
        x = self.title
        characters_to_remove = '<,>,:,",/,\,|,?,*,.'
        for character in characters_to_remove:
            x = x.replace(character, "")
        return f'tv-series/{x}/images/{filename}'

    imdb_id = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    release_year = models.CharField(max_length=10, null=True, blank=True)
    num_seasons = models.PositiveSmallIntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='genres')
    poster = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    poster_url = models.URLField(blank=True, null=True)
    trailer = models.URLField()
    rating = models.FloatField()
    cast = models.ManyToManyField(Actor, related_name='casts')
    director = models.ManyToManyField(Producer, related_name='directors')
    episodes = models.ManyToManyField('Episode', related_name='episodes', blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    MPAA_rating = models.CharField(choices=MPAA, max_length=4, default='G')
    view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    fetch_data = models.BooleanField(default=False)
    is_continuing = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('Series_Watch_View', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = create_slug_series(self.title)

    # @property
    # def detailed_picture_show(self):
    #     if self.poster:
    #         return mark_safe(f'<img src={self.poster.url}></img>')
    #     return mark_safe(f'<h3> No image to show </h3>')

        # if self.poster_url:
        #     # path = 'media/' + self.upload_file_name(self.title) + '.jpg'
        #     # parts = path.rsplit('/', 1)
        #     # result = f"{parts[0]}/{'/'.join(parts[1].split('/')[:-1])}"
        #     # os.makedirs(result)
        #     url = self.poster_url
        #     response = requests.get(url)
        #     image = Image.open(BytesIO(response.content))
        #     image = image.resize((285, 437), Image.ANTIALIAS)
        #     filestream = BytesIO()
        #     image.save(filestream, 'JPEG')
        #     filestream.seek(0)
        #     self.poster.save(self.poster_url.split('/')[-1], File(filestream), save=False)


# @receiver(pre_save, sender=TVSeries)
# def update_tvseries_fields(sender, instance, **kwargs):
#     if instance.IMDbid:
#         ia = IMDb()
#         imdb_data = ia.get_movie(instance.IMDbid)
#         genres = imdb_data['genres']
#
#         # populate other fields based on retrieved data
#         # instance.genre.set([Genre.objects.get_or_create(name=genre)[0] for genre in genres])
#         instance.name = imdb_data.get('title')
#         # instance.release_date = imdb_data.get('year')
#         instance.num_seasons = imdb_data['seasons']
#         instance.description = imdb_data.get('plot outline')
#         instance.poster_url = imdb_data.get('full-size cover url')
#         instance.rating = imdb_data.get('rating')
#         # instance.trailer = imdb_data.get('trailer')


class Episode(models.Model):
    " 'director', 'episode', 'episode title', 'full-size cover url', 'cast', "
    " 'original air date', 'producer', 'rating', 'runtimes', 'season', "
    "'title', 'writer', 'year'"
    def upload_file_name(self, filename):
        x = self.title
        characters_to_remove = '<,>,:,",/,\,|,?,*,.'
        tvseries = self.tv_series.title
        for character in characters_to_remove:
            x = x.replace(character, "")
        return f'tv-series/{tvseries}/{x}/images/{filename}'
    imdb_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, )
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, default=1)
    season = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    duration = models.DurationField()
    description = models.TextField()
    rating = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    original_air_date = models.CharField(max_length=50, null=True, blank=True)
    cast = models.ManyToManyField(Actor, blank=True)
    director = models.ManyToManyField(Producer, related_name='director_producer', blank=True)
    writer = models.ManyToManyField(Producer, related_name='writer_producer', blank=True)
    producer = models.ManyToManyField(Producer, related_name='producer_producer', blank=True)
    cover = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    cover_url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    episode_view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} (Season {self.season}, Episode {self.episode_number})"

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('Episode_Watch_View', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = create_slug_series(self.title)


class DailySeriesViews(models.Model):
    tv_series = models.ForeignKey(TVSeries, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)


def create_slug_series(title):
    # Generate a slug from the title using Django's slugify function
    slug = slugify(title)
    # Limit the slug length to 50 characters
    slug = slug[:50]
    return slug


class DailySeriesEpisodeViews(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)













