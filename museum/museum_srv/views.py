from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoStandPage, VideoStandEmployee, VideoStandCurrentEmployee, TimeLine, \
    TimeLineCurrentYear, FlowMask, AreaSamara, AreaSamaraCurrentStage, Technologies, TechnologiesCurrentStage, \
    TechnologiesFourth, TechnologiesCurrentLabel, EntryGroupVideo, AreaSamaraAutoPlay, Idle
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
                VideoStandPage.objects.all().delete()
                VideoStandPage.objects.create(page=request.data['page'])
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

    def post(self, request) -> Response:
        # handles post-requests from the app, sets a list of the honorable employees
        try:
            employee_list = request.data['employees']
            current_list = VideoStandEmployee.objects.all().values('fio')
            fio_list = [employee['fio'] for employee in current_list]
            for employee in employee_list:
                group = employee['group']
                fio = employee['fio']
                job = employee['job']
                description = employee['description']
                photo = employee['photo']
                order = employee['order']
                if fio in fio_list:
                    VideoStandEmployee.objects.filter(fio=fio).update(group=group, fio=fio, job=job,
                                                                      description=description,
                                                                      photo=photo, order=order)
                else:
                    VideoStandEmployee.objects.create(group=group, fio=fio, job=job, description=description,
                                                      photo=photo, order=order)
            return Response()
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
                VideoStandCurrentEmployee.objects.all().delete()
                VideoStandCurrentEmployee.objects.create(current_employee=request.data['current_employee'])
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
            else:
                TimeLineCurrentYear.objects.all().delete()
                TimeLineCurrentYear.objects.create(current_year=request.data['year'])
            cache.set(self.year_key, request.data['year'])
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TimeLineVideoAPIView(APIView):
    """Video by selected year and necessary index (first or second - there are two videos for each of years)"""

    def get(self, request, year: [int, str], video_index: int) -> Response:
        # handles get-requests from the second app, returns video path, intro video path and their durations:
        # you should specify one of the following years: 1936, 1953, 1961, 1970, 1980s, 1990s, 2000s, 2010s and
        # video index: 1 or 2
        try:
            video = TimeLine.objects.filter(year=year).values \
                (f'video_{video_index}', f'video_{video_index}_duration',
                 f'intro_video_{video_index}', f'intro_video_{video_index}_duration').first()

            video_path = video[f'video_{video_index}']
            final_path = f'/media/{video_path}'
            duration = video[f'video_{video_index}_duration']

            intro_video_path = video[f'intro_video_{video_index}']
            final_intro_path = f'/media/{intro_video_path}'
            intro_duration = video[f'intro_video_{video_index}_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}",
                             "intro_video": f"{final_intro_path}",
                             "intro_video_duration": f"{intro_duration}"
                             })
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class FlowMaskAPIView(APIView):
    """Flows"""
    mask_key = 'flow_mask'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns a mask for on and off flows
        current_mask = cache.get(self.mask_key)
        if not current_mask:
            mask = bin(int(str(FlowMask.objects.first())))[2:].zfill(7)
            cache.set(self.mask_key, mask)
            current_mask = mask
        return Response({"mask": f"{current_mask}"})

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets a mask for on and off flows
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
        else:
            FlowMask.objects.all().delete()
            FlowMask.objects.create(mask=new_mask)
        cache.set(self.mask_key, bin(new_mask)[2:].zfill(7))
        return Response()


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
                AreaSamaraAutoPlayAPIView.post(AreaSamaraAutoPlayAPIView, request, 0)
            elif count_of_records == 1:
                AreaSamaraCurrentStage.objects.update(stage=request.data['stage'])
                AreaSamaraAutoPlayAPIView.post(AreaSamaraAutoPlayAPIView, request, 0)
            else:
                AreaSamaraCurrentStage.objects.all().delete()
                AreaSamaraCurrentStage.objects.create(stage=request.data['stage'])
                AreaSamaraAutoPlayAPIView.post(AreaSamaraAutoPlayAPIView, request, 0)
            cache.set(self.stage_key, request.data['stage'])
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
                cache.set(self.autoplay_key, autoplay_condition)
                current_condition = autoplay_condition
            return Response({"auto_play": f"{current_condition}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request, condition) -> Response:
        # handles post-request from the controllers or from server (after stage changing in AreaSamara),
        # you should specify autoplay condition: 1 or 0
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


class TechnologiesStageAPIView(APIView):
    """Selected stage in Technologies"""
    stage_key = 'technologies_stage'

    def get(self, request) -> Response:
        # handles get-requests from the app with the backstage video, the moving screen and the control screen,
        # returns selected stage
        try:
            current_stage = cache.get(self.stage_key)
            if not current_stage:
                stage = TechnologiesCurrentStage.objects.first()
                cache.set(self.stage_key, stage)
                current_stage = stage
            return Response({"stage": f"{current_stage}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the tablet, sets selected stage
        try:
            count_of_records = TechnologiesCurrentStage.objects.count()
            if count_of_records == 0:
                TechnologiesCurrentStage.objects.create(stage=request.data['stage'])
            elif count_of_records == 1:
                TechnologiesCurrentStage.objects.update(stage=request.data['stage'])
            else:
                TechnologiesCurrentStage.objects.all().delete()
                TechnologiesCurrentStage.objects.create(stage=request.data['stage'])
            cache.set(self.stage_key, request.data['stage'])
            # request.get(controller_link)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesFourthAPIView(APIView):
    """Fourth stage in Technologies"""

    def get(self, request, label: str) -> Response:
        # handles get-requests from the moving screen, returns video path and its duration
        # according to specified label (that was specified in TechnologiesVideoLabelAPIView)
        try:
            fourth_video = TechnologiesFourth.objects \
                .filter(label=label).values('fourth_stage_video', 'fourth_stage_video_duration').first()
            fourth_video_path = fourth_video['fourth_stage_video']
            final_path = f'/media/{fourth_video_path}'

            duration = fourth_video['fourth_stage_video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesVideoLabelAPIView(APIView):
    """Video label for the selected video on the moving screen on the fourth stage in Technologies"""
    label_key = 'technologies_label'

    def get(self, request) -> Response:
        # handles get-requests from the moving screen, returns selected video label
        # (that was specified from the control screen in the method below)
        try:
            current_label = cache.get(self.label_key)
            if not current_label:
                label = TechnologiesCurrentLabel.objects.first()
                cache.set(self.label_key, label)
                current_label = label
            return Response({"label": f"{current_label}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

    def post(self, request) -> Response:
        # handles post-requests from the control screen, sets selected video label
        try:
            count_of_records = TechnologiesCurrentLabel.objects.count()
            if count_of_records == 0:
                TechnologiesCurrentLabel.objects.create(label=request.data['label'])
            elif count_of_records == 1:
                TechnologiesCurrentLabel.objects.update(label=request.data['label'])
            else:
                TechnologiesCurrentLabel.objects.all().delete()
                TechnologiesCurrentLabel.objects.create(label=request.data['label'])
            cache.set(self.label_key, request.data['label'])
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TechnologiesMovingAndBackstageAPIView(APIView):
    """Video on the moving screen on stages 1-3 (and at the beginning of the 4th) and the backstage video"""

    def get(self, request, video_type: str, stage: int) -> Response:
        # handles get-requests from the app with the backstage video and from the moving screen,
        # returns video path and its duration
        # according to video type (moving or backstage) and the stage (1, 2, 3 or 4)
        try:
            video = Technologies.objects \
                .filter(stage=stage).values(f'{video_type}_video', f'{video_type}_video_duration').first()
            video_path = video[f'{video_type}_video']
            final_path = f'/media/{video_path}'

            duration = video[f'{video_type}_video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class EntryGroupVideoAPIView(APIView):
    """Video in Entry Group"""

    def get(self, request) -> Response:
        # handles get-requests from the app, returns video path and its duration
        try:
            video = EntryGroupVideo.objects.values('video', 'video_duration').first()
            video_path = video['video']
            final_path = f'/media/{video_path}'

            duration = video[f'video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class IdleAPIView(APIView):
    """State, video and video duration for each app"""
    state_key = 'state_key'

    def get(self, request, app, field) -> Response:
        # handles get-request from the app, returns state or video and video duration (depends on param 'field'),
        # attention: it's necessary to define app name (param 'app') and field ('video' or 'state')!
        if field == 'state':
            try:
                current_state = cache.get(self.state_key)
                if not current_state:
                    state = Idle.objects.filter(app=app).values('state').first()['state']
                    cache.set(self.state_key, state)
                    current_state = state
                return Response({"state": f"{current_state}"})
            except DataBaseException:
                return Response(data="Unknown database error. Please, check tables and file models.py",
                                status=500, exception=True)
        if field == 'video':
            try:
                video = Idle.objects.filter(app=app).values('video', 'video_duration').first()
                video_path = video['video']
                final_path = f'/media/{video_path}'

                duration = video[f'video_duration']

                return Response({"current_video": f"{final_path}",
                                 "video_duration": f"{duration}"})
            except DataBaseException:
                return Response(data="Unknown database error. Please, check tables and file models.py",
                                status=500, exception=True)

    def post(self, request, app, state) -> Response:
        # handles post-request from the tablet, sets idle for the app
        try:
            count_of_records = Idle.objects.filter(app=app).count()
            if count_of_records == 0:
                Idle.objects.create(app=app, state=state)
            elif count_of_records == 1:
                Idle.objects.filter(app=app).update(app=app, state=state)
            else:
                Idle.objects.filter(app=app).delete()
                Idle.objects.create(app=app, state=state)
            cache.set(self.state_key, state)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)

