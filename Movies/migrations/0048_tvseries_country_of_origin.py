# Generated by Django 4.1.4 on 2023-05-23 10:06

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0047_alter_movie_mpaa_rating_alter_tvseries_mpaa_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvseries',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True),
        ),
    ]
