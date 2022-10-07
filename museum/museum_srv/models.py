from django.db import models
from model_utils import Choices
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR


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
    current_employee = models.CharField(max_length=100)

    def __str__(self):
        return self.fio


class TimeLine(models.Model):
    year = models.CharField(max_length=4)
    video_1 = models.FileField(upload_to='static/timeline/video')
    video_2 = models.FileField(upload_to='static/timeline/video')
    video_1_duration = models.CharField(max_length=100, blank=True)
    video_2_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TimeLine, self).save(*args, **kwargs)
        video_1 = self.video_1
        final_path_1 = f'media/{video_1}'
        clip_1 = VideoFileClip(os.path.join(BASE_DIR, final_path_1))
        video_1_duration = clip_1.duration
        TimeLine.objects.update(video_1_duration=video_1_duration)

        video_2 = self.video_2
        final_path_2 = f'media/{video_2}'
        clip_2 = VideoFileClip(os.path.join(BASE_DIR, final_path_2))
        video_2_duration = clip_2.duration
        TimeLine.objects.update(video_2_duration=video_2_duration)

    def __str__(self):
        return self.year


class AreaSamara(models.Model):
    pipeline = models.CharField(max_length=100)
    video = models.FileField(upload_to='static/area_samara/video')
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(AreaSamara, self).save(*args, **kwargs)
        video = self.video
        final_path = f'media/{video}'
        clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
        video_duration = clip.duration
        AreaSamara.objects.update(video_duration=video_duration)

    def __str__(self):
        return self.pipeline


class Technologies(models.Model):
    stage = models.CharField(max_length=100)
    backstage_video = models.FileField(upload_to='static/technologies/video')
    backstage_video_duration = models.CharField(max_length=100, blank=True)
    moving_video = models.FileField(upload_to='static/technologies/video')
    moving_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(Technologies, self).save(*args, **kwargs)

        backstage_video = self.backstage_video
        back_final_path = f'media/{backstage_video}'
        back_clip = VideoFileClip(os.path.join(BASE_DIR, back_final_path))
        back_video_duration = back_clip.duration
        Technologies.objects.update(backstage_video_duration=back_video_duration)

        moving_video = self.moving_video
        mov_final_path = f'media/{moving_video}'
        mov_clip = VideoFileClip(os.path.join(BASE_DIR, mov_final_path))
        mov_video_duration = mov_clip.duration
        Technologies.objects.update(moving_video_duration=mov_video_duration)

    def __str__(self):
        return self.stage


class TechnologiesFourth(models.Model):
    label = models.CharField(max_length=100)
    fourth_stage_video = models.FileField(upload_to='static/technologies/video')
    fourth_stage_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TechnologiesFourth, self).save(*args, **kwargs)
        fourth_stage_video = self.fourth_stage_video
        final_path = f'media/{fourth_stage_video}'
        clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
        video_duration = clip.duration
        TechnologiesFourth.objects.update(fourth_stage_video_duration=video_duration)


class FlowMask(models.Model):
    mask = models.CharField(max_length=9)

    def __str__(self):
        return self.mask
