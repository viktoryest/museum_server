from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile
from moviepy.editor import VideoFileClip
from museum.settings import BASE_DIR
from django.core.validators import FileExtensionValidator
from museum_srv.modules.laurent import change_technology_move, set_handle_technology_action
import os


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
        list_of_stages = ['past', 'present_1', 'present_2', 'present_3', 'future']
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


class TechnologiesLaurent:
    target_stage = None
    current_stage = None
    current_moving_mode = "stop"
    stages = ['past', 'present_1', 'present_2', 'present_3', 'future']

    @classmethod
    def subscribe_events(cls):
        set_handle_technology_action(cls.change_current_stage)

    @classmethod
    def move_to_stage(cls, stage: str):
        if (stage is not None) and (stage not in cls.stages):
            raise ValueError(f'Unknown stage: {cls.target_stage}. Available stages: {cls.stages}')

        if cls.target_stage == stage:
            return

        cls.target_stage = stage

        cls.handle_move()

    @classmethod
    def change_current_stage(cls, stage: str):
        if (stage is not None) and (stage not in cls.stages):
            raise ValueError(f'Unknown stage: {cls.target_stage}. Available stages: {cls.stages}')

        if cls.current_stage == stage:
            return

        print(f'Changing current stage {cls.current_stage} -> {stage}')

        cls.current_stage = stage

        cls.handle_move()

    @classmethod
    def handle_move(cls):
        # going nowhere, we will automatically stop at the ends of the rail
        if cls.target_stage is None:
            return

        # we are outside all dimensions
        if cls.current_stage is None:
            # and we are not moving
            if cls.current_moving_mode == "stop":
                # moving to the left
                cls.current_moving_mode = "left"
                change_technology_move("left")
            return

        # we are reached target stage
        if cls.target_stage == cls.current_stage:
            cls.target_stage = None
            cls.current_moving_mode = "stop"
            change_technology_move("stop")
            return

        # if index of target stage is less than index of current stage, move to the left
        if cls.stages.index(cls.target_stage) < cls.stages.index(cls.current_stage):
            cls.current_moving_mode = "left"
            change_technology_move("left")
            return

        # if index of target stage is greater than index of current stage, move to the right
        if cls.stages.index(cls.target_stage) > cls.stages.index(cls.current_stage):
            cls.current_moving_mode = "right"
            change_technology_move("right")
            return
