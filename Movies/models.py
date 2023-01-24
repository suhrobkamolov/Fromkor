from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

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

# G- General Audiences

MPAA = (
    ('G', 'General Audiences'),
    ('PG', 'Parental Guidance Suggested'),
    ('PG13', 'Parents Strongly Cautioned'),
    ('R', 'Restricted'),
    ('NC17', 'No Children 17 and Under Admitted'),
)


class Category(models.Model):
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
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


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
        return reverse('products:product_list_by_category', args=[self.company_slug])

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
        return reverse('products:product_list_by_category', args=[self.producer_slug])

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
        return reverse('products:product_list_by_category', args=[self.actor_slug])


class Movie(models.Model):
    slug = models.SlugField(unique=True)
    movie_title = models.CharField(max_length=120)
    movie_year = models.PositiveIntegerField(default=2023,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
        help_text="Use the following format: <YYYY>")
    movie_release_date = models.DateField()
    movie_duration = models.CharField(max_length=50, help_text='1h 20m')
    movie_MPAA_rating = models.CharField(choices=MPAA, max_length=4, default='G')
    movie_genre = models.ManyToManyField(Category, default='UNDEFINED')
    movie_imdb = models.FloatField(default=5.0)
    movie_producer = models.ManyToManyField(Producer, default='UNDEFINED')
    movie_company = models.ManyToManyField(Company, default='UNDEFINED')
    movie_topic = models.CharField(max_length=120)
    movie_language = models.CharField(choices=STATUS_CHOICES, default=":)", max_length=120)
    movie_actors = models.ManyToManyField(Actor, default='/N')
    movie_image = models.FileField(upload_to='templates/images/movies/', null=True, blank=True)
    thumb_url = models.CharField(max_length=500, null=True, blank=True)
    thumb = models.FileField(upload_to='images/products/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    movie_status = models.CharField(max_length=120, null=True, blank=True)
    movie_view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

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
        return reverse('products:product_detail', args=[self.slug])


class Comment(models.Model):
    product = models.ForeignKey(Movie, on_delete=models.CASCADE)


def create_slug(instance, new_slag = None):
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









