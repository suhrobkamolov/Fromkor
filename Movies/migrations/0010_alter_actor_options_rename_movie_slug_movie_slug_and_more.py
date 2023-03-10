# Generated by Django 4.1.4 on 2023-01-14 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0009_alter_movie_movie_actors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'ordering': ['-created_at'], 'verbose_name': 'Actor', 'verbose_name_plural': 'Actors'},
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='movie_slug',
            new_name='slug',
        ),
        migrations.AlterIndexTogether(
            name='movie',
            index_together={('id', 'slug')},
        ),
    ]
