# Generated by Django 4.0.2 on 2022-02-27 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_videos_caption_videos_date_videos_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='subtitle',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
