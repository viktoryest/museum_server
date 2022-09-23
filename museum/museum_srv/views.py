from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, TimeLine, AreaSamara, Technologies, TechnologiesMoving
from django.shortcuts import redirect


class VideoStandPageAPIView(APIView):
    def get(self, request):
        page = VideoStandPage.objects.first()
        return Response({"page": f"{page}"})

    def post(self, request):
        VideoStandPage.objects.update(page=request.data['page'])
        return Response()


class VideoStandEmployeeAPIView(APIView):
    def get(self, request, group):
        employee_list = \
            VideoStandEmployee.objects.filter(group=group).values("id", "fio", "job", "description", "photo")
        return Response({"employees": employee_list})


class TimeLineAPIView(APIView):
    def get(self, request):
        year = TimeLine.objects.first()
        return Response({"year": f"{year}"})

    def post(self, request):
        TimeLine.objects.update(year=request.data['year'])
        return Response()


class TimeLineVideoAPIView(APIView):
    def get(self, request, year, video):
        video_index = video
        video = TimeLine.objects.filter(year=year).values(f'video_{video_index}')
        video_path = video.first()[f'video_{video_index}']
        final_path = f'/media/{video_path}'
        return final_path


class AreaSamaraAPIView(APIView):
    def get(self, request):
        pipeline = AreaSamara.objects.first()
        return Response({"pipeline": f"{pipeline}"})

    def post(self, request):
        AreaSamara.objects.update(pipeline=request.data['pipeline'])
        # request.get(controller_link)
        return Response()


class AreaSamaraVideoAPIView(APIView):
    def get(self, request):
        video = AreaSamara.objects.filter(pk=1).values('video')
        video_path = video.first()['video']
        final_path = f'/media/{video_path}'
        return final_path


class TechnologiesAPIView(APIView):
    def get(self, request):
        stage = Technologies.objects.filter(pk=1).values('stage')
        return Response({"stage": f"{stage}"})

    def post(self, request):
        Technologies.objects.update(stage=request.data['stage'])
        # request.get(controller_link)
        return Response()


class TechnologiesVideoAPIView(APIView):
    def get(self, request):
        backstage_video = Technologies.objects.filter(pk=1).values('backstage_video')
        backstage_video_path = backstage_video.first()['backstage_video']
        final_path = f'/media/{backstage_video_path}'
        return final_path


class TechnologiesVideoLabelAPIView(APIView):
    def get(self, request):
        label = TechnologiesMoving.objects.filter(pk=1).values('label')
        return Response({"label": f"{label}"})

    def post(self, request):
        TechnologiesMoving.objects.update(label=request.data['label'])
        return Response()


class TechnologiesMovingVideoAPIView(APIView):
    def get(self, request, label):
        moving_video = TechnologiesMoving.objects.filter(label=label).values('moving_video')
        moving_video_path = moving_video.first()['moving_video']
        final_path = f'/media/{moving_video_path}'
        return final_path
