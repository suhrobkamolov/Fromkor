# Generated by Django 4.1.4 on 2023-01-14 17:54

from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0002_movie_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_status',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('RA', 'Recently Added'), ('MW', 'Most Watched'), ('TR', 'Top Rated')], default=django.utils.timezone.now, max_length=5),
            preserve_default=False,
        ),
    ]
