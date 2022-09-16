from rest_framework import serializers
from .models import VideoStandPage


class VideoStandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoStandPage
        fields = '__all__'
