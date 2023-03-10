# Generated by Django 4.1.4 on 2023-02-09 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0018_movie_movie_trailer_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMovieViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movies.movie')),
            ],
        ),
    ]
