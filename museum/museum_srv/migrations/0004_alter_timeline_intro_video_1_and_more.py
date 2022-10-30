# Generated by Django 4.1.1 on 2022-10-28 20:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0003_timeline_intro_video_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='intro_video_1',
            field=models.FileField(upload_to='static/timeline/video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='intro_video_2',
            field=models.FileField(upload_to='static/timeline/video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]
