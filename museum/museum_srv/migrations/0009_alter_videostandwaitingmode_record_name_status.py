# Generated by Django 4.1.1 on 2023-03-27 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_srv', '0008_alter_videostandwaitingmode_record_name_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videostandwaitingmode',
            name='record_name_status',
            field=models.BooleanField(default=True),
        ),
    ]
