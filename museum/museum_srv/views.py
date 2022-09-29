from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, TimeLine, AreaSamara, Technologies, TechnologiesMoving, FlowMask
from django.core.cache import cache
# import requests - for sending a request to the controller


class VideoStandPageAPIView(APIView):
    page_key = 'video_stand_page'

    def get(self, request):
        current_page = cache.get(self.page_key)
        if not current_page:
            page = VideoStandPage.objects.first()
            cache.set(self.page_key, page)
        return Response({"page": f"{current_page}"})

    def post(self, request):
        VideoStandPage.objects.update(page=request.data['page'])
        cache.set(self.page_key, request.data['page'])
        return Response()


class VideoStandEmployeeAPIView(APIView):
    employee_key = 'video_stand_employee'

    def get(self, request, group):
        current_employee_list = cache.get(self.employee_key)
        if not current_employee_list:
            employee_list = \
                VideoStandEmployee.objects.filter(group=group).values("id", "fio", "job", "description", "photo")
            cache.set(self.employee_key, employee_list)
        return Response({"employees": current_employee_list})


class TimeLineAPIView(APIView):
    year_key = 'timeline_year'

    def get(self, request):
        current_year = cache.get(self.year_key)
        if not current_year:
            year = TimeLine.objects.first()
            cache.set(self.year_key, year)
        return Response({"year": f"{current_year}"})

    def post(self, request):
        TimeLine.objects.update(year=request.data['year'])
        cache.set(self.year_key, request.data['year'])
        return Response()


class TimeLineVideoAPIView(APIView):
    video_key = 'timeline_video'

    def get(self, request, year, video):
        video_index = video
        current_video = cache.get(self.video_key)
        if not current_video:
            video = TimeLine.objects.filter(year=year).values(f'video_{video_index}')
            video_path = video.first()[f'video_{video_index}']
            final_path = f'/media/{video_path}'
            cache.set(self.video_key, final_path)
        return current_video


class AreaSamaraAPIView(APIView):
    pipeline_key = 'area_samara_pipeline'

    def get(self, request):
        current_pipeline = cache.get(self.pipeline_key)
        if not current_pipeline:
            pipeline = AreaSamara.objects.first()
            cache.set(self.pipeline_key, pipeline)
        return Response({"pipeline": f"{current_pipeline}"})

    def post(self, request):
        AreaSamara.objects.update(pipeline=request.data['pipeline'])
        cache.set(self.pipeline_key, request.data['pipeline'])
        # requests.get(controller_link)
        return Response()


class AreaSamaraVideoAPIView(APIView):
    video_key = 'area_samara_video'

    def get(self, request):
        current_video = cache.get(self.video_key)
        if not current_video:
            video = AreaSamara.objects.filter(pk=1).values('video')
            video_path = video.first()['video']
            final_path = f'/media/{video_path}'
            cache.set(self.video_key, final_path)
        return current_video


class TechnologiesAPIView(APIView):
    stage_key = 'technologies_stage'

    def get(self, request):
        current_stage = cache.get(self.stage_key)
        if not current_stage:
            stage = Technologies.objects.filter(pk=1).values('stage')
            cache.set(self.stage_key, stage)
        return Response({"stage": f"{current_stage}"})

    def post(self, request):
        Technologies.objects.update(stage=request.data['stage'])
        cache.set(self.stage_key, request.data['stage'])
        # request.get(controller_link)
        return Response()


class TechnologiesVideoAPIView(APIView):
    video_key = 'technologies_video'

    def get(self, request):
        current_video = cache.get(self.video_key)
        if not current_video:
            backstage_video = Technologies.objects.filter(pk=1).values('backstage_video')
            backstage_video_path = backstage_video.first()['backstage_video']
            final_path = f'/media/{backstage_video_path}'
            cache.set(self.video_key, final_path)
        return current_video


class TechnologiesVideoLabelAPIView(APIView):
    label_key = 'technologies_label'

    def get(self, request):
        current_label = cache.get(self.label_key)
        if not current_label:
            label = TechnologiesMoving.objects.filter(pk=1).values('label')
            cache.set(self.label_key, label)
        return Response({"label": f"{current_label}"})

    def post(self, request):
        TechnologiesMoving.objects.update(label=request.data['label'])
        cache.set(self.label_key,  request.data['label'])
        return Response()


class TechnologiesMovingVideoAPIView(APIView):
    moving_video_key = 'technologies_moving_video'

    def get(self, request, label):
        current_video = cache.get(self.moving_video_key)
        if not current_video:
            moving_video = TechnologiesMoving.objects.filter(label=label).values('moving_video')
            moving_video_path = moving_video.first()['moving_video']
            final_path = f'/media/{moving_video_path}'
            cache.set(self.moving_video_key, final_path)
        return current_video


class FlowMaskAPIView(APIView):
    mask_key = 'flow_mask'

    def get(self, request):
        current_mask = cache.get(self.mask_key)
        if not current_mask:
            mask = bin(int(str(FlowMask.objects.first())))
            cache.set(self.mask_key, mask)
        return Response({"mask": f"{current_mask}"})

    def post(self, request, flow, condition):
        mask = int(str(FlowMask.objects.first()), base=2)
        print(mask, type(mask))
        position = int(flow) - 1
        if condition == 'on':
            new_mask = mask | (1 << position)
            FlowMask.objects.update(mask=new_mask)
            cache.set(self.mask_key, new_mask)
        elif condition == 'off':
            new_mask = mask & ~(1 << position)
            FlowMask.objects.update(mask=new_mask)
            cache.set(self.mask_key, new_mask)
        return Response()
