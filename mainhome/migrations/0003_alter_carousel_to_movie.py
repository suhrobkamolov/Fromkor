# Generated by Django 4.1.4 on 2023-01-30 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0015_alter_movie_movie_image'),
        ('mainhome', '0002_rename_movie_carousel_to_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='to_movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CarouselItem', to='Movies.movie'),
        ),
    ]
