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
        employee_list = None
        if group == "fame":
            employee_list = \
                VideoStandEmployee.objects.filter(group="fame").values("id", "fio", "job", "description", "photo")
        elif group == "veterans":
            employee_list = \
                VideoStandEmployee.objects.filter(group="veterans").values("id", "fio", "job", "description", "photo")
        # else:
        #     raise ValueError('The group is not found')
        return Response({"employees": employee_list})
