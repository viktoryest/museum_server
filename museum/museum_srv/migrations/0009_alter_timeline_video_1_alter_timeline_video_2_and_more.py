# Generated by Django 4.1.1 on 2022-09-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0008_alter_timeline_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='video_1',
            field=models.FileField(upload_to='media/static/timeline/video'),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='video_2',
            field=models.FileField(upload_to='media/static/timeline/video'),
        ),
        migrations.AlterField(
            model_name='videostandemployee',
            name='photo',
            field=models.ImageField(upload_to='media/static/employees/images'),
        ),
    ]
