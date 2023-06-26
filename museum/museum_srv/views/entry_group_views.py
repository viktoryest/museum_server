from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.entry_group_models import EntryGroupVideo
from exceptions import DataBaseException


class EntryGroupVideoAPIView(APIView):
    """Video in Entry Group"""

    def get(self, request) -> Response:
        # handles get-requests from the app, returns video path and its duration
        try:
            video = EntryGroupVideo.objects.values('video', 'video_duration').first()
            video_path = video['video']
            final_path = f'/{video_path}'

            duration = video[f'video_duration']

            return Response({"current_video": f"{final_path}",
                             "video_duration": f"{duration}"})
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)
