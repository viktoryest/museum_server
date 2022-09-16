from django.shortcuts import render
from rest_framework import generics
from .models import VideoStandPage
from .serializers import VideoStandSerializer


class VideoStandAPIView(generics.ListAPIView):
    queryset = VideoStandPage.objects.all()
    serializer_class = VideoStandSerializer
