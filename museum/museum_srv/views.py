from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, TimeLine, AreaSamara, Technologies, FlowMask, TechnologiesFourth
from django.core.cache import cache


# import requests - for sending a request to the controller


class VideoStandPageAPIView(APIView):
    page_key = 'video_stand_page'

    def get(self, request):
        current_page = cache.get(self.page_key)
        if not current_page:
            page = VideoStandPage.objects.first()
            cache.set(self.page_key, page)
            current_page = page
        return Response({"page": f"{current_page}"})

    def post(self, request):
        if VideoStandPage.objects.count() == 0:
            VideoStandPage.objects.create(page=request.data['page'])
        elif VideoStandPage.objects.count() == 1:
            VideoStandPage.objects.update(page=request.data['page'])
        cache.set(self.page_key, request.data['page'])
        return Response()


class VideoStandEmployeeListAPIView(APIView):
    def get(self, request, group):
        employee_list = \
            VideoStandEmployee.objects.filter(group=group).values("id", "fio", "job", "description", "photo")
        return Response({"employees": employee_list})


class VideoStandEmployeeAPIView(APIView):
    employee_key = 'video_stand_employee'

    def get(self, request):
        current_employee = cache.get(self.employee_key)
        if not current_employee:
            employee = VideoStandEmployee.objects.filter(pk=1).values("current_employee")
            cache.set(self.employee_key, employee)
            current_employee = employee
        return Response({"employee": f"{current_employee}"})

    def post(self, request):
        if VideoStandEmployee.objects.count() == 0:
            VideoStandEmployee.objects.create(current_employee=request.data['current_employee'])
        elif VideoStandEmployee.objects.count() == 1:
            VideoStandEmployee.objects.update(current_employee=request.data['current_employee'])
        cache.set(self.employee_key, request.data['current_employee'])
        return Response()


class TimeLineAPIView(APIView):
    year_key = 'timeline_year'

    def get(self, request):
        current_year = cache.get(self.year_key)
        if not current_year:
            year = TimeLine.objects.first()
            cache.set(self.year_key, year)
            current_year = year
        return Response({"year": f"{current_year}"})

    def post(self, request):
        if TimeLine.objects.count() == 0:
            TimeLine.objects.create(year=request.data['year'])
        elif TimeLine.objects.count() == 1:
            TimeLine.objects.update(year=request.data['year'])
        cache.set(self.year_key, request.data['year'])
        return Response()


class TimeLineVideoAPIView(APIView):
    def get(self, request, year, video):
        video_index = video
        video = TimeLine.objects.filter(year=year).values(f'video_{video_index}')
        video_path = video.first()[f'video_{video_index}']
        final_path = f'/media/{video_path}'

        duration = \
            TimeLine.objects.filter(year=year).values(f'video_{video_index}_duration').first() \
                [f'video_{video_index}_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class AreaSamaraAPIView(APIView):
    pipeline_key = 'area_samara_pipeline'

    def get(self, request):
        current_pipeline = cache.get(self.pipeline_key)
        if not current_pipeline:
            pipeline = AreaSamara.objects.first()
            cache.set(self.pipeline_key, pipeline)
            current_pipeline = pipeline
        return Response({"pipeline": f"{current_pipeline}"})

    def post(self, request):
        if AreaSamara.objects.count() == 0:
            AreaSamara.objects.create(pipeline=request.data['pipeline'])
        elif AreaSamara.objects.count() == 1:
            AreaSamara.objects.update(pipeline=request.data['pipeline'])
        cache.set(self.pipeline_key, request.data['pipeline'])
        # requests.get(controller_link)
        return Response()


class AreaSamaraVideoAPIView(APIView):
    def get(self, request):
        video = AreaSamara.objects.filter(pk=1).values('video')
        video_path = video.first()['video']
        final_path = f'/media/{video_path}'

        duration = AreaSamara.objects.filter(pk=1).values('video_duration').first()['video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesStageAPIView(APIView):
    stage_key = 'technologies_stage'

    def get(self, request):
        current_stage = cache.get(self.stage_key)
        if not current_stage:
            stage = Technologies.objects.filter(pk=1).values('stage')
            cache.set(self.stage_key, stage)
            current_stage = stage
        return Response({"stage": f"{current_stage}"})

    def post(self, request):
        if Technologies.objects.count() == 0:
            Technologies.objects.create(stage=request.data['stage'])
        elif Technologies.objects.count() == 1:
            Technologies.objects.update(stage=request.data['stage'])
        cache.set(self.stage_key, request.data['stage'])
        # request.get(controller_link)
        return Response()


class TechnologiesFourthAPIView(APIView):
    def get(self, request, label):
        fourth_video = TechnologiesFourth.objects \
            .filter(label=label).values("fourth_stage_video", "fourth_stage_video_duration")
        fourth_video_path = fourth_video.first()['fourth_stage_video']
        final_path = f'/media/{fourth_video_path}'

        duration = TechnologiesFourth.objects \
            .filter(label=label).values('fourth_stage_video_duration').first()['fourth_stage_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesVideoLabelAPIView(APIView):
    label_key = 'technologies_label'

    def get(self, request):
        current_label = cache.get(self.label_key)
        if not current_label:
            label = TechnologiesFourth.objects.values('label').first()['label']
            cache.set(self.label_key, label)
            current_label = label
        return Response({"label": f"{current_label}"})

    def post(self, request):
        if TechnologiesFourth.objects.count() == 0:
            TechnologiesFourth.objects.create(label=request.data['label'])
        elif TechnologiesFourth.objects.count() == 1:
            TechnologiesFourth.objects.update(label=request.data['label'])
        cache.set(self.label_key, request.data['label'])
        return Response()


class TechnologiesMovingAPIView(APIView):
    def get(self, request, stage):
        moving_video = Technologies.objects \
            .filter(stage=stage).values("moving_video", "moving_video_duration")
        moving_video_path = moving_video.first()['moving_video']
        final_path = f'/media/{moving_video_path}'

        duration = Technologies.objects \
            .filter(stage=stage).values('moving_video_duration').first()['moving_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesBackstageAPIView(APIView):
    def get(self, request, stage):
        backstage_video = Technologies.objects \
            .filter(stage=stage).values("backstage_video", "backstage_video_duration")
        backstage_video_path = backstage_video.first()['backstage_video']
        final_path = f'/media/{backstage_video_path}'

        duration = Technologies.objects \
            .filter(stage=stage).values('backstage_video_duration').first()['backstage_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class FlowMaskAPIView(APIView):
    mask_key = 'flow_mask'

    def get(self, request):
        current_mask = cache.get(self.mask_key)
        if not current_mask:
            mask = bin(int(str(FlowMask.objects.first())))
            cache.set(self.mask_key, mask)
            current_mask = mask
        return Response({"mask": f"{current_mask}"})

    def post(self, request):
        mask = int(str(FlowMask.objects.first()))
        position = int(request.data['flow']) - 1
        if request.data['condition'] and type(request.data['condition']) == bool:
            new_mask = mask | (1 << position)
            if FlowMask.objects.count() == 0:
                FlowMask.objects.create(mask=new_mask)
            elif FlowMask.objects.count() == 1:
                FlowMask.objects.update(mask=new_mask)
            cache.set(self.mask_key, bin(new_mask)[2:])
        elif not request.data['condition'] and type(request.data['condition']) == bool:
            new_mask = mask & ~(1 << position)
            if FlowMask.objects.count() == 0:
                FlowMask.objects.create(mask=new_mask)
            elif FlowMask.objects.count() == 1:
                FlowMask.objects.update(mask=new_mask)
            cache.set(self.mask_key, bin(new_mask)[2:])
        return Response()
