# Generated by Django 4.1.1 on 2022-09-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0004_videostandemployee_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videostandemployee',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
