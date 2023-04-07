from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.area_samara_models import AreaSamara, AreaSamaraCurrentStage, AreaSamaraAutoPlay
from django.core.cache import cache
from exceptions import DataBaseException


class AreaSamaraStageAPIView(APIView):
    """Selected stage in Area Samara"""
    stage_key = 'area_samara_stage'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns selected stage
        try:
            current_stage = cache.get(self.stage_key)
            if not current_stage:
                stage = AreaSamaraCurrentStage.objects.first()
                cache.set(self.stage_key, stage)
                current_stage = stage
            return Response({"stage": f"{current_stage}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets selected stage
        try:
            count_of_records = AreaSamaraCurrentStage.objects.count()
            stage = request.data['stage']
            if count_of_records == 0:
                AreaSamaraCurrentStage.objects.create(stage=stage)
            elif count_of_records == 1:
                AreaSamaraCurrentStage.objects.update(stage=stage)
            else:
                AreaSamaraCurrentStage.objects.all().delete()
                AreaSamaraCurrentStage.objects.create(stage=stage)
            cache.set(self.stage_key, stage)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class AreaSamaraVideoAPIView(APIView):
    """Video in Area Samara"""

    def get(self, request, stage: int) -> Response:
        # handles get-request from the app, returns video path and its duration,
        # you should specify the number of the stage: 1, 2, 3 or 4
        try:
            video = AreaSamara.objects.filter(stage=f'stage_{stage}').values('video', 'video_duration').first()
            video_path = video['video']
            final_path = f'/media/{video_path}'

            duration = video['video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class AreaSamaraAutoPlayAPIView(APIView):
    """AutoPlay condition"""
    autoplay_key = 'area_samara_autoplay'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns autoplay condition: 1 or 0
        try:
            current_condition = cache.get(self.autoplay_key)
            if not current_condition:
                autoplay_condition = AreaSamaraAutoPlay.objects.first()
                cache.set(self.autoplay_key, autoplay_condition.auto_play)
                current_condition = autoplay_condition.auto_play
            return Response({"auto_play": current_condition})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-request from the controllers or from server (after stage changing in AreaSamara),
        # you should specify autoplay condition: 1 or 0
        condition = request.data['condition']
        try:
            count_of_records = AreaSamaraAutoPlay.objects.count()
            if count_of_records == 0:
                AreaSamaraAutoPlay.objects.create(auto_play=condition)
            elif count_of_records == 1:
                AreaSamaraAutoPlay.objects.update(auto_play=condition)
            else:
                AreaSamaraAutoPlay.objects.all().delete()
                AreaSamaraAutoPlay.objects.create(auto_play=condition)
            cache.set(self.autoplay_key, condition)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
