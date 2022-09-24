"""museum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from museum_srv.views import VideoStandPageAPIView, VideoStandEmployeeAPIView, TimeLineAPIView, TimeLineVideoAPIView, \
    AreaSamaraAPIView, AreaSamaraVideoAPIView, TechnologiesAPIView, TechnologiesVideoAPIView, \
    TechnologiesMovingVideoAPIView, TechnologiesVideoLabelAPIView, FlowMaskAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video_stand/', VideoStandPageAPIView.as_view()),
    path('api/video_stand/page/', VideoStandPageAPIView.as_view()),
    path('api/video_stand/employee/<group>/', VideoStandEmployeeAPIView.as_view()),
    path('api/timeline/year/', TimeLineAPIView.as_view()),
    path('api/timeline/<int:year>/<int:video>/', TimeLineVideoAPIView.as_view()),
    path('api/area_samara/pipeline/', AreaSamaraAPIView.as_view()),
    path('api/area_samara/video/', AreaSamaraVideoAPIView.as_view()),
    path('api/technologies/stage/', TechnologiesAPIView.as_view()),
    path('api/technologies/video/', TechnologiesVideoAPIView.as_view()),
    path('api/technologies/moving_video_label/', TechnologiesVideoLabelAPIView.as_view()),
    path('api/technologies/moving_video/<label>/', TechnologiesMovingVideoAPIView.as_view()),
    path('api/flows/condition/', FlowMaskAPIView.as_view()),
    path('api/flows/<int:flow>/<condition>/', FlowMaskAPIView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
