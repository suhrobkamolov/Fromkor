# Generated by Django 4.1.4 on 2023-03-19 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0032_rename_category_genre_alter_genre_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvseries',
            name='episodes',
            field=models.ManyToManyField(blank=True, related_name='episodes', to='Movies.episode'),
        ),
    ]