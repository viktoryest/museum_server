# Generated by Django 4.1.1 on 2022-10-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0022_timelinecurrentyear'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaSamaraCurrentStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_stage', models.CharField(max_length=10)),
            ],
        ),
    ]