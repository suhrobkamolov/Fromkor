# Generated by Django 4.1.4 on 2023-03-29 23:32

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0042_movie_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='votes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='run_time',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
