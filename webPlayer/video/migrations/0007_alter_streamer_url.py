# Generated by Django 4.0.2 on 2022-04-01 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_alter_streamer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='url',
            field=models.URLField(blank=True, default='', max_length=255, null=True),
        ),
    ]
