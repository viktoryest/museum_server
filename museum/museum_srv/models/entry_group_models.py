from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from model_utils import Choices
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator


class EntryGroupVideo(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = EntryGroupVideo.objects.all().values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    video = models.FileField(upload_to='static/entry_group/video',
                             validators=[FileExtensionValidator(allowed_extensions=["mp4"]), check_file_existence])
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(EntryGroupVideo, self).save(*args, **kwargs)
        video = self.video
        if video:
            final_path = f'media/{video}'
            if os.path.isfile(final_path):
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
