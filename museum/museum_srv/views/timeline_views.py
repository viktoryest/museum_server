from rest_framework.response import Response
from rest_framework.views import APIView
from museum_srv.models.timeline_models import TimeLine, TimeLineCurrentYear
from django.core.cache import cache
from exceptions import DataBaseException


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
            current_year = request.data['year']
            if count_of_records == 0:
                TimeLineCurrentYear.objects.create(current_year=current_year)
            elif count_of_records == 1:
                TimeLineCurrentYear.objects.update(current_year=current_year)
            else:
                TimeLineCurrentYear.objects.all().delete()
                TimeLineCurrentYear.objects.create(current_year=current_year)
            cache.set(self.year_key, current_year)
            return Response()
        except DataBaseException:
            return Response(data="Unknown database error. Please, check tables and file models.py",
                            status=500, exception=True)


class TimeLineVideoAPIView(APIView):
    """Video by selected year and necessary index (first or second - there are two videos for each of years)"""

    def get(self, request, year: [int, str], video_index: int) -> Response:
        # handles get-requests from the second app, returns video path, intro video path and their durations:
        # you should specify one of the following years: 1936, 1953, 1961, 1970, 1980s, 1990s, 2000s, 2010s, VIP and
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
