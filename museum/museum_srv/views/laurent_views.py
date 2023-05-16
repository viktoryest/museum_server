from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.idle_models import Idle
from django.core.cache import cache
from exceptions import DataBaseException


# Laurent can send only GET-request to the server, so we need separate view for it

class LaurentAPISamaraView(APIView):
    """State, video and video duration for each app"""
    idle_state_key = 'state_key'

    def get(self, request):
        app = "samara"
        app_cache_key = f'{self.idle_state_key}_{app}'

        data = False

        try:
            count_of_records = Idle.objects.filter(app=app).count()
            if count_of_records == 0:
                Idle.objects.create(app=app, state=data)
            elif count_of_records == 1:
                data = not Idle.objects.filter(app=app).values('state').first()['state']
                Idle.objects.filter(app=app).update(app=app, state=data)
            else:
                Idle.objects.filter(app=app).delete()
                Idle.objects.create(app=app, state=data)
            cache.set(app_cache_key, data)
            return Response(data=data)
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
