from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, TimeLine


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


class VideoStandEmployeePhotoAPIView(APIView):
    def get(self, request, fio):
        employee_photo = VideoStandEmployee.objects.filter(fio=fio).values("photo")
        return Response(employee_photo)


class TimeLineAPIView(APIView):
    def get(self, request):
        year = TimeLine.objects.first()
        return Response({"year": f"{year}"})

    def post(self, request):
        TimeLine.objects.update(year=request.data['year'])
        return Response()

