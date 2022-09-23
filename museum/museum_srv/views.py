from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, TimeLine, AreaSamara
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
        response = redirect(f'/media/{video_path}')
        return response


class AreaSamaraAPIView(APIView):
    def get(self, request):
        pipeline = AreaSamara.objects.first()
        return Response({"pipeline": f"{pipeline}"})

    def post(self, request):
        AreaSamara.objects.update(pipeline=request.data['pipeline'])
        return Response()


class AreaSamaraVideoAPIView(APIView):
    def get(self, request):
        video = AreaSamara.objects.filter(pk=1).values('video')
        video_path = video.first()['video']
        print(video_path)
        response = redirect(f'/media/{video_path}')
        return response
