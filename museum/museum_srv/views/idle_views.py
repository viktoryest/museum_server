from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.idle_models import Idle
from django.core.cache import cache
from exceptions import DataBaseException


class IdleAPIView(APIView):
    """State, video and video duration for each app"""
    state_key = 'state_key'

    def get(self, request, app, field) -> Response:
        app_cache_key = f'{self.state_key}_{app}'
        # handles get-request from the app, returns state or video and video duration (depends on param 'field'),
        # attention: it's necessary to define app name (param 'app') and field ('video' or 'state')!
        if field == 'state':
            try:
                current_state = cache.get(app_cache_key)
                if not current_state:
                    state = Idle.objects.filter(app=app).values('state').first()['state']
                    cache.set(app_cache_key, state)
                    current_state = state
                return Response({"state": current_state})
            except DataBaseException:
                return Response(data="Unknown database error. Please, check tables and file models.py",
                                status=500, exception=True)
        if field == 'video':
            try:
                video = Idle.objects.filter(app=app).values('video', 'video_duration').first()
                video_path = video['video']
                final_path = f'/{video_path}'

                duration = video[f'video_duration']

                return Response({"current_video": f"{final_path}",
                                 "video_duration": f"{duration}"})
            except DataBaseException:
                return Response(data="Unknown database error. Please, check tables and file models.py",
                                status=500, exception=True)

    def post(self, request, app) -> Response:
        app_cache_key = f'{self.state_key}_{app}'
        # handles post-request from the tablet, sets idle for the app
        data = request.data['state']
        try:
            count_of_records = Idle.objects.filter(app=app).count()
            if count_of_records == 0:
                Idle.objects.create(app=app, state=data)
            elif count_of_records == 1:
                Idle.objects.filter(app=app).update(app=app, state=data)
            else:
                Idle.objects.filter(app=app).delete()
                Idle.objects.create(app=app, state=data)
            cache.set(app_cache_key, data)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
