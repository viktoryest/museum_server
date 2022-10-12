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
        count_of_records = VideoStandPage.objects.count()
        if count_of_records == 0:
            VideoStandPage.objects.create(page=request.data['page'])
        elif count_of_records == 1:
            VideoStandPage.objects.update(page=request.data['page'])
        cache.set(self.page_key, request.data['page'])
        return Response()


class VideoStandEmployeeListAPIView(APIView):
    def get(self, request, group):
        employee_list = \
            VideoStandEmployee.objects.filter(group=group).values('id', 'fio', 'job', 'description', 'photo')
        return Response({"employees": employee_list})


class VideoStandEmployeeAPIView(APIView):
    employee_key = 'video_stand_employee'

    def get(self, request):
        current_employee = cache.get(self.employee_key)
        if not current_employee:
            employee = VideoStandEmployee.objects.first()
            cache.set(self.employee_key, employee)
            current_employee = employee
        return Response({"employee": f"{current_employee}"})

    def post(self, request):
        count_of_records = VideoStandEmployee.objects.count()
        if count_of_records == 0:
            VideoStandEmployee.objects.create(current_employee=request.data['current_employee'])
        elif count_of_records == 1:
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
        count_of_records = TimeLine.objects.count()
        if count_of_records == 0:
            TimeLine.objects.create(year=request.data['year'])
        elif count_of_records == 1:
            TimeLine.objects.update(year=request.data['year'])
        cache.set(self.year_key, request.data['year'])
        return Response()


class TimeLineVideoAPIView(APIView):
    def get(self, request, year, video_index):
        video = TimeLine.objects.filter(year=year).values \
            (f'video_{video_index}', f'video_{video_index}_duration').first()
        video_path = video[f'video_{video_index}']
        final_path = f'/media/{video_path}'

        duration = video[f'video_{video_index}_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class AreaSamaraAPIView(APIView):
    stage_key = 'area_samara_stage'

    def get(self, request):
        current_stage = cache.get(self.stage_key)
        if not current_stage:
            stage = AreaSamara.objects.first()
            cache.set(self.stage_key, stage)
            current_stage = stage
        return Response({"stage": f"{current_stage}"})

    def post(self, request):
        count_of_records = AreaSamara.objects.count()
        if count_of_records == 0:
            AreaSamara.objects.create(stage=request.data['stage'])
        elif count_of_records == 1:
            AreaSamara.objects.update(stage=request.data['stage'])
        cache.set(self.stage_key, request.data['stage'])
        # requests.get(controller_link)
        return Response()


class AreaSamaraVideoAPIView(APIView):
    def get(self, request, stage):
        video = AreaSamara.objects.filter(stage=stage).values('video', 'video_duration').first()
        video_path = video['video']
        final_path = f'/media/{video_path}'

        duration = video['video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesStageAPIView(APIView):
    stage_key = 'technologies_stage'

    def get(self, request):
        current_stage = cache.get(self.stage_key)
        if not current_stage:
            stage = Technologies.objects.first()
            cache.set(self.stage_key, stage)
            current_stage = stage
        return Response({"stage": f"{current_stage}"})

    def post(self, request):
        count_of_records = Technologies.objects.count()
        if count_of_records == 0:
            Technologies.objects.create(stage=request.data['stage'])
        elif count_of_records == 1:
            Technologies.objects.update(stage=request.data['stage'])
        cache.set(self.stage_key, request.data['stage'])
        # request.get(controller_link)
        return Response()


class TechnologiesFourthAPIView(APIView):
    def get(self, request, label):
        fourth_video = TechnologiesFourth.objects \
            .filter(label=label).values('fourth_stage_video', 'fourth_stage_video_duration').first()
        fourth_video_path = fourth_video['fourth_stage_video']
        final_path = f'/media/{fourth_video_path}'

        duration = fourth_video['fourth_stage_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesVideoLabelAPIView(APIView):
    label_key = 'technologies_label'

    def get(self, request):
        current_label = cache.get(self.label_key)
        if not current_label:
            label = TechnologiesFourth.objects.first()
            cache.set(self.label_key, label)
            current_label = label
        return Response({"label": f"{current_label}"})

    def post(self, request):
        count_of_records = TechnologiesFourth.objects.count()
        if count_of_records == 0:
            TechnologiesFourth.objects.create(label=request.data['label'])
        elif count_of_records == 1:
            TechnologiesFourth.objects.update(label=request.data['label'])
        cache.set(self.label_key, request.data['label'])
        return Response()


class TechnologiesMovingAndBackstageAPIView(APIView):
    def get(self, request, video_type, stage):
        video = Technologies.objects \
            .filter(stage=stage).values(f'{video_type}_video', f'{video_type}_video_duration').first()
        video_path = video[f'{video_type}_video']
        final_path = f'/media/{video_path}'

        duration = video[f'{video_type}_video_duration']

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
        new_mask = None
        if request.data['condition'] and type(request.data['condition']) == bool:
            new_mask = mask | (1 << position)
        elif not request.data['condition'] and type(request.data['condition']) == bool:
            new_mask = mask & ~(1 << position)
        count_of_records = FlowMask.objects.count()
        if count_of_records == 0:
            FlowMask.objects.create(mask=new_mask)
        elif count_of_records == 1:
            FlowMask.objects.update(mask=new_mask)
        cache.set(self.mask_key, bin(new_mask)[2:])
        return Response()
