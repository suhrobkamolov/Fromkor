# Generated by Django 4.1.4 on 2023-02-26 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0024_episode_created_episode_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='fetch_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tvseries',
            name='fetch_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tvseries',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
