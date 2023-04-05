from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator


class Technologies(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = Technologies.objects.filter(stage=path.instance.stage).values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    stage = models.CharField(max_length=100)
    backstage_video = models.FileField(upload_to='static/technologies/video',
                                       validators=[FileExtensionValidator(allowed_extensions=["mp4"]),
                                                   check_file_existence])
    backstage_video_duration = models.CharField(max_length=100, blank=True)
    moving_video = models.FileField(upload_to='static/technologies/video', blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=["mp4"]),
                                                check_file_existence])
    moving_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(Technologies, self).save(*args, **kwargs)
        backstage_video = self.backstage_video
        if backstage_video:
            back_final_path = f'media/{backstage_video}'
            if os.path.isfile(back_final_path):
                back_clip = VideoFileClip(os.path.join(BASE_DIR, back_final_path))
                back_video_duration = back_clip.duration
                Technologies.objects.filter(stage=self.stage).update(backstage_video_duration=back_video_duration)

        moving_video = self.moving_video
        if moving_video:
            mov_final_path = f'media/{moving_video}'
            if os.path.isfile(mov_final_path):
                mov_clip = VideoFileClip(os.path.join(BASE_DIR, mov_final_path))
                mov_video_duration = mov_clip.duration
                Technologies.objects.filter(stage=self.stage).update(moving_video_duration=mov_video_duration)

    @classmethod
    def check_technologies_stages(cls):
        list_of_stages = ['past', 'present_1', 'present_2', 'future']
        for stage in list_of_stages:
            if not cls.objects.filter(stage=stage):
                cls.objects.create(stage=stage)

    def __str__(self):
        return self.stage


class TechnologiesCurrentStage(models.Model):
    stage = models.CharField(max_length=100)

    def __str__(self):
        return self.stage


class TechnologiesFourth(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = TechnologiesFourth.objects.filter(label=path.instance.label).values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    label = models.CharField(max_length=100)
    fourth_stage_video = models.FileField(upload_to='static/technologies/video',
                                          validators=[FileExtensionValidator(allowed_extensions=["mp4"]),
                                                      check_file_existence])
    fourth_stage_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TechnologiesFourth, self).save(*args, **kwargs)
        fourth_stage_video = self.fourth_stage_video
        if fourth_stage_video:
            final_path = f'media/{fourth_stage_video}'
            if os.path.isfile(final_path):
                clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
                video_duration = clip.duration
                TechnologiesFourth.objects.filter(label=self.label).update(fourth_stage_video_duration=video_duration)

    def __str__(self):
        return self.label


class TechnologiesCurrentLabel(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label
