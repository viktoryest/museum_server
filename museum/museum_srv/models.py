from django.db import models
from model_utils import Choices
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from exceptions import *


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


class TimeLine(models.Model):
    year = models.CharField(max_length=10)
    video_1 = models.FileField(upload_to='static/timeline/video')
    video_2 = models.FileField(upload_to='static/timeline/video')
    video_1_duration = models.CharField(max_length=100, blank=True)
    video_2_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TimeLine, self).save(*args, **kwargs)
        video_1 = self.video_1
        if video_1:
            final_path_1 = f'media/{video_1}'
            clip_1 = VideoFileClip(os.path.join(BASE_DIR, final_path_1))
            video_1_duration = clip_1.duration
            TimeLine.objects.filter(year=self.year).update(video_1_duration=video_1_duration)

        video_2 = self.video_2
        if video_2:
            final_path_2 = f'media/{video_2}'
            clip_2 = VideoFileClip(os.path.join(BASE_DIR, final_path_2))
            video_2_duration = clip_2.duration
            TimeLine.objects.filter(year=self.year).update(video_2_duration=video_2_duration)

    @classmethod
    def check_timeline_videos(cls):
        list_of_years = ['1936', '1953', '1961', '1970', '1980s', '1990s', '2000s', '2010s']
        for year in list_of_years:
            if not cls.objects.filter(year=year):
                cls.objects.create(year=year)

    def __str__(self):
        return self.year


class TimeLineCurrentYear(models.Model):
    current_year = models.CharField(max_length=10)

    def __str__(self):
        return self.current_year


class FlowMask(models.Model):
    mask = models.CharField(max_length=9)

    @classmethod
    def check_flows(cls):
        count_of_records = cls.objects.count()
        if count_of_records == 0:
            cls.objects.create(mask='0000000')

    def __str__(self):
        return self.mask


class AreaSamara(models.Model):
    stage = models.CharField(max_length=100)
    video = models.FileField(upload_to='static/area_samara/video')
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(AreaSamara, self).save(*args, **kwargs)
        video = self.video
        if video:
            final_path = f'media/{video}'
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


class Technologies(models.Model):
    stage = models.CharField(max_length=100)
    backstage_video = models.FileField(upload_to='static/technologies/video')
    backstage_video_duration = models.CharField(max_length=100, blank=True)
    moving_video = models.FileField(upload_to='static/technologies/video')
    moving_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(Technologies, self).save(*args, **kwargs)
        backstage_video = self.backstage_video
        if backstage_video:
            back_final_path = f'media/{backstage_video}'
            back_clip = VideoFileClip(os.path.join(BASE_DIR, back_final_path))
            back_video_duration = back_clip.duration
            Technologies.objects.filter(stage=self.stage).update(backstage_video_duration=back_video_duration)

        moving_video = self.moving_video
        if moving_video:
            mov_final_path = f'media/{moving_video}'
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
    label = models.CharField(max_length=100)
    fourth_stage_video = models.FileField(upload_to='static/technologies/video')
    fourth_stage_video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TechnologiesFourth, self).save(*args, **kwargs)
        fourth_stage_video = self.fourth_stage_video
        final_path = f'media/{fourth_stage_video}'
        clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
        video_duration = clip.duration
        TechnologiesFourth.objects.filter(label=self.label).update(fourth_stage_video_duration=video_duration)

    def __str__(self):
        return self.label


class TechnologiesCurrentLabel(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class EntryGroupVideo(models.Model):
    video = models.FileField(upload_to='static/entry_group/video')
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(EntryGroupVideo, self).save(*args, **kwargs)
        video = self.video
        if video:
            final_path = f'media/{video}'
            clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
            video_duration = clip.duration
            EntryGroupVideo.objects.filter(video=self.video).update(video_duration=video_duration)

    @classmethod
    def check_entry_group_video(cls):
        count_of_records = cls.objects.count()
        if count_of_records == 0:
            cls.objects.create()

    def __str__(self):
        return 'Entry Group Video'
