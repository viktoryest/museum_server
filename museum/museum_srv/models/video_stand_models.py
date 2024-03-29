from django.db import models
from model_utils import Choices


class VideoStandPage(models.Model):
    page = models.CharField(max_length=50)

    def __str__(self):
        return self.page


class VideoStandEmployee(models.Model):
    group = models.CharField(max_length=50, choices=Choices('fame', 'veterans'))
    fio = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='static/employees/images')
    order = models.IntegerField()

    def __str__(self):
        return self.fio


class VideoStandCurrentEmployee(models.Model):
    current_employee = models.CharField(max_length=100)

    def __str__(self):
        return self.current_employee
