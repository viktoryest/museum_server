from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from moviepy.editor import VideoFileClip
import os
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator


class Idle(models.Model):
    def check_file_existence(path: FieldFile):
        complete_path = f'media/{str(path)}'
        if path:
            field_name = str(path.field).split('.')[-1]
            local_path = os.path.join(BASE_DIR, complete_path)
            current_field_value = Idle.objects.filter(app=path.instance.app).values(field_name) \
                .first().values()
            if path in current_field_value and not os.path.isfile(local_path):
                path.delete()
                raise ValidationError(f'Please, check video in {field_name}. Possibly, it was deleted manually')

    app = models.CharField(max_length=50)
    state = models.BooleanField()
    video = models.FileField(upload_to=f'static/idle/video',
                             validators=[FileExtensionValidator(allowed_extensions=["mp4"]), check_file_existence])
    video_duration = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(Idle, self).save(*args, **kwargs)
        video = self.video
        if video:
            final_path = f'media/{video}'
            if os.path.isfile(final_path):
                clip = VideoFileClip(os.path.join(BASE_DIR, final_path))
                video_duration = clip.duration
                Idle.objects.filter(app=self.app).update(video_duration=video_duration)

    @classmethod
    def check_idle_videos(cls):
        list_of_apps = ['human_capital', 'timeline', 'samara', 'flows', 'technology']
        for app in list_of_apps:
            if not cls.objects.filter(app=app):
                cls.objects.create(app=app, state=0)

    def __str__(self):
        return self.app
