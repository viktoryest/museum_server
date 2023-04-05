from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.video_stand_models import VideoStandPage, VideoStandEmployee, VideoStandCurrentEmployee
from django.core.cache import cache
from exceptions import DataBaseException


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
            page = request.data['page']
            if count_of_records == 0:
                VideoStandPage.objects.create(page=page)
            elif count_of_records == 1:
                VideoStandPage.objects.update(page=page)
            else:
                VideoStandPage.objects.all().delete()
                VideoStandPage.objects.create(page=page)
            cache.set(self.page_key, page)
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
            current_employee = request.data['current_employee']
            if count_of_records == 0:
                VideoStandCurrentEmployee.objects.create(current_employee=current_employee)
            elif count_of_records == 1:
                VideoStandCurrentEmployee.objects.update(current_employee=current_employee)
            else:
                VideoStandCurrentEmployee.objects.all().delete()
                VideoStandCurrentEmployee.objects.create(current_employee=current_employee)
            cache.set(self.employee_key, current_employee)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
