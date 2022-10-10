# Generated by Django 4.1.1 on 2022-10-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0018_rename_technologiesmoving_technologieslabel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologiesFourth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('fourth_stage_video', models.FileField(upload_to='static/technologies/video')),
                ('fourth_stage_video_duration', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='TechnologiesLabel',
        ),
        migrations.AddField(
            model_name='technologies',
            name='moving_video',
            field=models.FileField(default=20, upload_to='static/technologies/video'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='technologies',
            name='moving_video_duration',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]