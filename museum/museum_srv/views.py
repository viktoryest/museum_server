from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, VideoStandCurrentEmployee, TimeLine, TimeLineCurrentYear, \
    AreaSamara, AreaSamaraCurrentStage, Technologies, FlowMask, TechnologiesFourth
from django.core.cache import cache
from exceptions import *


# import requests - for sending a request to the controller


class VideoStandPageAPIView(APIView):
    """Current chapter in Video Stand"""
    page_key = 'video_stand_page'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns selected page (chapter)
        # attention: if page hasn't been selected, will be returned None instead of current_page
        try:
            current_page = cache.get(self.page_key)
            if not current_page:
                page = VideoStandPage.objects.first()
                cache.set(self.page_key, page)
                current_page = page
            return Response({"page": f"{current_page}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets selected page (chapter)
        try:
            count_of_records = VideoStandPage.objects.count()
            if count_of_records == 0:
                VideoStandPage.objects.create(page=request.data['page'])
            elif count_of_records == 1:
                VideoStandPage.objects.update(page=request.data['page'])
            else:
                raise OverInstancesException("The count of VideoStandPage instances is more than 1. "
                                             "Most likely, some of them were added manually. Please, check your tables "
                                             "and delete extra records to avoid mistakes")
            cache.set(self.page_key, request.data['page'])
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class VideoStandEmployeeListAPIView(APIView):
    """Honorable employees list in Video Stand"""

    def get(self, request, group: str) -> Response:
        # handles get-requests from the app, returns a list of the honorable employees,
        # that contains id, fio(surname, name, patronymic), job, description, path to the photo;
        # you should specify the group in the parameters: it might be "fame" or "veterans"
        try:
            employee_list = \
                VideoStandEmployee.objects.filter(group=group).values('id', 'fio', 'job', 'description', 'photo')
            return Response({"employees": employee_list})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class VideoStandEmployeeAPIView(APIView):
    """Selected employee in Video Stand"""
    employee_key = 'video_stand_employee'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns selected employee
        # attention: if employee hasn't been selected, will be returned None instead of current_employee
        try:
            current_employee = cache.get(self.employee_key)
            if not current_employee:
                employee = VideoStandCurrentEmployee.objects.first()
                cache.set(self.employee_key, employee)
                current_employee = employee
            return Response({"employee": f"{current_employee}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-request from the tablet, sets selected employee
        try:
            count_of_records = VideoStandCurrentEmployee.objects.count()
            if count_of_records == 0:
                VideoStandCurrentEmployee.objects.create(current_employee=request.data['current_employee'])
            elif count_of_records == 1:
                VideoStandCurrentEmployee.objects.update(current_employee=request.data['current_employee'])
            else:
                raise OverInstancesException("The count of VideoStandCurrentEmployee instances is more than 1. "
                                             "Most likely, some of them were added manually. Please, check your tables "
                                             "and delete extra records to avoid mistakes")
            cache.set(self.employee_key, request.data['current_employee'])
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TimeLineYearAPIView(APIView):
    """Selected year in Timeline"""
    year_key = 'timeline_year'

    def get(self, request) -> Response:
        # handles get-requests from the second app, returns selected year
        # attention: if year hasn't been selected, will be returned None instead of current_year
        try:
            current_year = cache.get(self.year_key)
            if not current_year:
                year = TimeLineCurrentYear.objects.first()
                cache.set(self.year_key, year)
                current_year = year
            return Response({"year": f"{current_year}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the first app, sets selected year
        try:
            count_of_records = TimeLineCurrentYear.objects.count()
            if count_of_records == 0:
                TimeLineCurrentYear.objects.create(current_year=request.data['year'])
            elif count_of_records == 1:
                TimeLineCurrentYear.objects.update(current_year=request.data['year'])
            cache.set(self.year_key, request.data['year'])
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TimeLineVideoAPIView(APIView):
    """Video by selected year and necessary index (first or second - there are two videos for each of years)"""

    def get(self, request, year: [int, str], video_index: int) -> Response:
        # handles get-requests from the second app, returns video path and its duration:
        # you should specify one of the following years: 1936, 1953, 1961, 1970, 1980s, 1990s, 2000s, 2010s and
        # video index: 1 or 2
        try:
            video = TimeLine.objects.filter(year=year).values \
                (f'video_{video_index}', f'video_{video_index}_duration').first()
            video_path = video[f'video_{video_index}']
            final_path = f'/media/{video_path}'

            duration = video[f'video_{video_index}_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class FlowMaskAPIView(APIView):
    """Flows"""
    mask_key = 'flow_mask'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns a mask for on and off flows
        # attention: if mask hasn't been set, will be returned None instead of mask
        try:
            current_mask = cache.get(self.mask_key)
            if not current_mask:
                mask = FlowMask.objects.first()
                cache.set(self.mask_key, mask)
                current_mask = mask
            return Response({"mask": f"{current_mask}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets a mask for on and off flows
        try:
            mask = int(str(FlowMask.objects.first()))
            position = int(request.data['flow']) - 1
            new_mask = None
            if request.data['condition'] and type(request.data['condition']) == bool:
                new_mask = bin(mask | (1 << position))[2:].zfill(8)
            elif not request.data['condition'] and type(request.data['condition']) == bool:
                new_mask = bin(mask & ~(1 << position))[2:].zfill(8)
            count_of_records = FlowMask.objects.count()
            if count_of_records == 0:
                FlowMask.objects.create(mask=new_mask)
            elif count_of_records == 1:
                FlowMask.objects.update(mask=new_mask)
            cache.set(self.mask_key, new_mask)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


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
            if count_of_records == 0:
                AreaSamaraCurrentStage.objects.create(stage=request.data['stage'])
            elif count_of_records == 1:
                AreaSamaraCurrentStage.objects.update(stage=request.data['stage'])
            cache.set(self.stage_key, request.data['stage'])
            # requests.get(controller_link)
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
            video = AreaSamara.objects.filter(stage=stage).values('video', 'video_duration').first()
            video_path = video['video']
            final_path = f'/media/{video_path}'

            duration = video['video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesStageAPIView(APIView):
    """Selected stage in Technologies"""
    stage_key = 'technologies_stage'

    def get(self, request) -> Response:
        # handles get-requests from the app with the backstage video, the moving screen and the control screen,
        # returns selected stage
        current_stage = cache.get(self.stage_key)
        if not current_stage:
            stage = Technologies.objects.first()
            cache.set(self.stage_key, stage)
            current_stage = stage
        return Response({"stage": f"{current_stage}"})

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets selected stage
        count_of_records = Technologies.objects.count()
        if count_of_records == 0:
            Technologies.objects.create(stage=request.data['stage'])
        elif count_of_records == 1:
            Technologies.objects.update(stage=request.data['stage'])
        cache.set(self.stage_key, request.data['stage'])
        # request.get(controller_link)
        return Response()


class TechnologiesFourthAPIView(APIView):
    """Fourth stage in Technologies"""

    def get(self, request, label: str) -> Response:
        # handles get-requests from the moving screen, returns video path and its duration
        # according to specified label (that was specified in TechnologiesVideoLabelAPIView)
        fourth_video = TechnologiesFourth.objects \
            .filter(label=label).values('fourth_stage_video', 'fourth_stage_video_duration').first()
        fourth_video_path = fourth_video['fourth_stage_video']
        final_path = f'/media/{fourth_video_path}'

        duration = fourth_video['fourth_stage_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})


class TechnologiesVideoLabelAPIView(APIView):
    """Video label for the selected video on the moving screen on the fourth stage in Technologies"""
    label_key = 'technologies_label'

    def get(self, request) -> Response:
        # handles get-requests from the moving screen, returns selected video label
        # (that was specified from the control screen in the method below)
        current_label = cache.get(self.label_key)
        if not current_label:
            label = TechnologiesFourth.objects.first()
            cache.set(self.label_key, label)
            current_label = label
        return Response({"label": f"{current_label}"})

    def post(self, request) -> Response:
        # handles post-requests from the control screen, sets selected video label
        count_of_records = TechnologiesFourth.objects.count()
        if count_of_records == 0:
            TechnologiesFourth.objects.create(label=request.data['label'])
        elif count_of_records == 1:
            TechnologiesFourth.objects.update(label=request.data['label'])
        cache.set(self.label_key, request.data['label'])
        return Response()


class TechnologiesMovingAndBackstageAPIView(APIView):
    """Video on the moving screen on stages 1-3 (and at the beginning of the 4th) and the backstage video"""

    def get(self, request, video_type: str, stage: int) -> Response:
        # handles get-requests from the app with the backstage video and from the moving screen,
        # returns video path and its duration
        # according to video type (moving or backstage) and the stage (1, 2, 3 or 4)
        video = Technologies.objects \
            .filter(stage=stage).values(f'{video_type}_video', f'{video_type}_video_duration').first()
        video_path = video[f'{video_type}_video']
        final_path = f'/media/{video_path}'

        duration = video[f'{video_type}_video_duration']

        return Response({"current_video": f"{final_path}",
                         "video_duration": f"{duration}"})
