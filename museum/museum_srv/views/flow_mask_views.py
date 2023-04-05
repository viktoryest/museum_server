from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.flow_mask_models import FlowMask
from django.core.cache import cache
from exceptions import DataBaseException
import threading

flowsLock = threading.Lock()


class FlowMaskAPIView(APIView):
    """Flows"""
    mask_key = 'flow_mask'

    def get(self, request) -> Response:
        # handles get-requests from the app, returns a mask for on and off flows
        with flowsLock:
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
        condition = request.data['condition']
        if condition and type(condition) == bool:
            new_mask = mask | (1 << position)
        elif not condition and type(condition) == bool:
            new_mask = mask & ~(1 << position)
        with flowsLock:
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


class WholeMaskAPIView(APIView):
    """Listening to Laurant and changing mask"""
    mask_key = 'flow_mask'

    def post(self, request, mask) -> Response:
        # handles post-requests, sets the mask entirely
        try:
            new_mask = int(mask, base=2)
            with flowsLock:
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
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
