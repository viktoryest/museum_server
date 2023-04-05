from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator


class TimeLine(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = TimeLine.objects.filter(year=path.instance.year).values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    year = models.CharField(max_length=10)
    video_1 = models.FileField(upload_to='static/timeline/video',
                               validators=[FileExtensionValidator(allowed_extensions=["mp4"]), check_file_existence])
    intro_video_1 = models.FileField(upload_to='static/timeline/video',
                                     validators=[FileExtensionValidator(allowed_extensions=["mp4"]),
                                                 check_file_existence])
    video_2 = models.FileField(upload_to='static/timeline/video',
                               validators=[FileExtensionValidator(allowed_extensions=["mp4"]), check_file_existence])
    intro_video_2 = models.FileField(upload_to='static/timeline/video',
                                     validators=[FileExtensionValidator(allowed_extensions=["mp4"]),
                                                 check_file_existence])
    video_1_duration = models.CharField(max_length=100, blank=True)
    intro_video_1_duration = models.CharField(max_length=100, blank=True)
    video_2_duration = models.CharField(max_length=100, blank=True)
    intro_video_2_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(TimeLine, self).save(*args, **kwargs)
        video_1 = self.video_1
        if video_1:
            final_path_1 = f'media/{video_1}'
            if os.path.isfile(final_path_1):
                clip_1 = VideoFileClip(os.path.join(BASE_DIR, final_path_1))
                video_1_duration = clip_1.duration
                TimeLine.objects.filter(year=self.year).update(video_1_duration=video_1_duration)

        intro_video_1 = self.intro_video_1
        if intro_video_1:
            final_path_intro_1 = f'media/{intro_video_1}'
            if os.path.isfile(final_path_intro_1):
                clip_intro_1 = VideoFileClip(os.path.join(BASE_DIR, final_path_intro_1))
                intro_video_1_duration = clip_intro_1.duration
                TimeLine.objects.filter(year=self.year).update(intro_video_1_duration=intro_video_1_duration)

        video_2 = self.video_2
        if video_2:
            final_path_2 = f'media/{video_2}'
            if os.path.isfile(final_path_2):
                clip_2 = VideoFileClip(os.path.join(BASE_DIR, final_path_2))
                video_2_duration = clip_2.duration
                TimeLine.objects.filter(year=self.year).update(video_2_duration=video_2_duration)

        intro_video_2 = self.intro_video_2
        if intro_video_2:
            final_path_intro_2 = f'media/{intro_video_2}'
            if os.path.isfile(final_path_intro_2):
                clip_intro_2 = VideoFileClip(os.path.join(BASE_DIR, final_path_intro_2))
                intro_video_2_duration = clip_intro_2.duration
                TimeLine.objects.filter(year=self.year).update(intro_video_2_duration=intro_video_2_duration)

    @classmethod
    def check_timeline_videos(cls):
        list_of_years = ['1936', '1953', '1961', '1970', '1974', '1979', '1980s', '1990s', '2000s', '2010s']
        for year in list_of_years:
            if not cls.objects.filter(year=year):
                cls.objects.create(year=year)

    def __str__(self):
        return self.year


class TimeLineCurrentYear(models.Model):
    current_year = models.CharField(max_length=10)

    def __str__(self):
        return self.current_year
