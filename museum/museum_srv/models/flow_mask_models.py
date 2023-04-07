from django.db import models


class FlowMask(models.Model):
    mask = models.CharField(max_length=9)

    @classmethod
    def check_flows(cls):
        count_of_records = cls.objects.count()
        if count_of_records == 0:
            cls.objects.create(mask='0000000')

    def __str__(self):
        return self.mask
