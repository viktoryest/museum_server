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
        list_of_stages = ['past', 'diaskan', 'volzhanka', 'future']
        for stage in list_of_stages:
            if not cls.objects.filter(stage=stage):
                cls.objects.create(stage=stage)
        # delete stages that are not in list_of_stages
        cls.objects.exclude(stage__in=list_of_stages).delete()

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


class TechnologiesModel:
    index: int | None = None
    frame: int = 0

    @classmethod
    def get_frame(cls):
        return cls.frame

    @classmethod
    def set_frame(cls, frame: int):
        cls.frame = frame

    @classmethod
    def get_index(cls):
        return cls.index

    @classmethod
    def set_index(cls, index: int | None):
        cls.index = index


class TechnologiesLaurent:
    target_point = None
    target_changed = False
    current_point = None
    last_point = None
    current_moving_mode = "stop"
    preparation = False
    points = ['past', 'present_1', 'present_2', 'present_3', 'future']

    @classmethod
    def point_from_stage(cls, stage: str):
        match stage:
            case 'past':
                return 'past'
            case 'diaskan':
                return 'present_1'
            case 'volzhanka':
                return 'present_3'
            case 'future':
                return 'future'

    @classmethod
    def subscribe_events(cls):
        set_handle_technology_action(cls.change_current_point)

    @classmethod
    def move_to_point(cls, point: str, preparation: bool = False):
        """
        :param point: point to move to
        :param preparation: True if we are in preparation mode, moving screen before starting the stage
        """
        if (point is not None) and (point not in cls.points):
            raise ValueError(f'Unknown point: {cls.target_point}. Available points: {cls.points}')

        cls.preparation = preparation

        if cls.target_point == point:
            return

        cls.target_point = point
        cls.target_changed = True

        cls.handle_move()

    @classmethod
    def change_current_point(cls, point: str):
        """ Set the point we are currently in
        :param point: point we are currently in
        """
        if (point is not None) and (point not in cls.points):
            raise ValueError(f'Unknown point: {cls.target_point}. Available points: {cls.points}')

        if cls.current_point == point:
            return

        print(f'Changing current point {cls.current_point} -> {point}')

        cls.last_point = cls.current_point
        cls.current_point = point

        cls.handle_move()

    @classmethod
    def handle_move(cls):
        # going nowhere, we will automatically stop at the ends of the rail
        if cls.target_point is None:
            return

        # we are outside all dimensions
        if cls.current_point is None:
            # and we have a new target
            if cls.target_changed:
                if cls.current_moving_mode == "stop" or cls.last_point is None:
                    # move to the left
                    cls.current_moving_mode = "left"
                    change_technology_move("left")
                elif cls.last_point == cls.target_point:
                    # return to last known point, move to the opposite side
                    mode = "right" if cls.current_moving_mode == "left" else "left"
                    cls.current_moving_mode = mode
                    change_technology_move(mode)
                else:
                    # move to another point
                    mode = cls.get_move_mode(cls.last_point, cls.target_point)
                    cls.current_moving_mode = mode
                    change_technology_move(mode)

            return

        move_mode = cls.get_move_mode(cls.current_point, cls.target_point)

        # we are reached target point
        if move_mode == "stop":
            cls.preparation = False
            cls.target_point = None

        cls.current_moving_mode = move_mode
        change_technology_move(move_mode)

    @classmethod
    def get_move_mode(cls, current_point: str, target_point: str):
        if target_point == current_point:
            return "stop"
        if cls.points.index(target_point) < cls.points.index(current_point):
            return "left"
        if cls.points.index(target_point) > cls.points.index(current_point):
            return "right"
