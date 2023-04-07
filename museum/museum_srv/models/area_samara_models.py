from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator


class AreaSamara(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = AreaSamara.objects.filter(stage=path.instance.stage).values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    stage = models.CharField(max_length=100)
    video = models.FileField(upload_to='static/area_samara/video',
                             validators=[FileExtensionValidator(allowed_extensions=["mp4"]), check_file_existence])
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(AreaSamara, self).save(*args, **kwargs)
        video = self.video
        if video:
            final_path = f'media/{video}'
            if os.path.isfile(final_path):
                clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
                video_duration = clip.duration
                AreaSamara.objects.filter(stage=self.stage).update(video_duration=video_duration)

    @classmethod
    def check_area_samara_stages(cls):
        list_of_stages = ['stage_1', 'stage_2', 'stage_3', 'stage_4']
        for stage in list_of_stages:
            if not cls.objects.filter(stage=stage):
                cls.objects.create(stage=stage)

    def __str__(self):
        return self.stage


class AreaSamaraCurrentStage(models.Model):
    stage = models.CharField(max_length=10)

    def __str__(self):
        return self.stage


class AreaSamaraAutoPlay(models.Model):
    auto_play = models.BooleanField()

    @classmethod
    def check_area_samara_auto_play(cls):
        count_of_records = cls.objects.count()
        if count_of_records == 0:
            cls.objects.create(auto_play=False)

    def __str__(self):
        return str(self.auto_play)
