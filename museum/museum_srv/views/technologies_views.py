from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.technologies_models import Technologies, TechnologiesCurrentStage, TechnologiesFourth, \
    TechnologiesCurrentLabel
from django.core.cache import cache
from exceptions import DataBaseException


class TechnologiesStageAPIView(APIView):
    """Selected stage in Technologies"""
    stage_key = 'technologies_stage'

    def get(self, request) -> Response:
        # handles get-requests from the app with the backstage video, the moving screen and the control screen,
        # returns selected stage
        try:
            current_stage = cache.get(self.stage_key)
            if not current_stage:
                stage = TechnologiesCurrentStage.objects.first()
                cache.set(self.stage_key, stage)
                current_stage = stage
            return Response({"stage": f"{current_stage}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets selected stage
        try:
            count_of_records = TechnologiesCurrentStage.objects.count()
            stage = request.data['stage']
            if count_of_records == 0:
                TechnologiesCurrentStage.objects.create(stage=stage)
            elif count_of_records == 1:
                TechnologiesCurrentStage.objects.update(stage=stage)
            else:
                TechnologiesCurrentStage.objects.all().delete()
                TechnologiesCurrentStage.objects.create(stage=stage)
            cache.set(self.stage_key, stage)
            # request.get(controller_link)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesFourthAPIView(APIView):
    """Fourth stage in Technologies"""

    def get(self, request, label: str) -> Response:
        # handles get-requests from the moving screen, returns video path and its duration
        # according to specified label (that was specified in TechnologiesVideoLabelAPIView)
        try:
            fourth_video = TechnologiesFourth.objects \
                .filter(label=label).values('fourth_stage_video', 'fourth_stage_video_duration').first()
            fourth_video_path = fourth_video['fourth_stage_video']
            final_path = f'/media/{fourth_video_path}'

            duration = fourth_video['fourth_stage_video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesVideoLabelAPIView(APIView):
    """Video label for the selected video on the moving screen on the fourth stage in Technologies"""
    label_key = 'technologies_label'

    def get(self, request) -> Response:
        # handles get-requests from the moving screen, returns selected video label
        # (that was specified from the control screen in the method below)
        try:
            current_label = cache.get(self.label_key)
            if not current_label:
                label = TechnologiesCurrentLabel.objects.first()
                cache.set(self.label_key, label)
                current_label = label
            return Response({"label": f"{current_label}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the control screen, sets selected video label
        try:
            count_of_records = TechnologiesCurrentLabel.objects.count()
            label = request.data['label']
            if count_of_records == 0:
                TechnologiesCurrentLabel.objects.create(label=label)
            elif count_of_records == 1:
                TechnologiesCurrentLabel.objects.update(label=label)
            else:
                TechnologiesCurrentLabel.objects.all().delete()
                TechnologiesCurrentLabel.objects.create(label=label)
            cache.set(self.label_key, label)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesMovingAndBackstageAPIView(APIView):
    """Video on the moving screen on stages 1-3 (and at the beginning of the 4th) and the backstage video"""

    def get(self, request, video_type: str, stage: int) -> Response:
        # handles get-requests from the app with the backstage video and from the moving screen,
        # returns video path and its duration
        # according to video type (moving or backstage) and the stage (1, 2, 3 or 4)
        try:
            video = Technologies.objects \
                .filter(stage=stage).values(f'{video_type}_video', f'{video_type}_video_duration').first()
            video_path = video[f'{video_type}_video']
            final_path = f'/media/{video_path}'

            duration = video[f'{video_type}_video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
