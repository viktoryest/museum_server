from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee


class VideoStandPageAPIView(APIView):
    def get(self, request):
        page = VideoStandPage.objects.filter(pk=1).values('page')[0]
        return Response(page)

    def post(self, request):
        VideoStandPage.objects.update(page=request.data['page'])
        return Response()


class VideoStandEmployeeAPIView(APIView):
    def get(self, request, group):
        employee_list = \
            VideoStandEmployee.objects.filter(group=group).values("id", "fio", "job", "description", "photo")
        return Response({"employees": employee_list})
