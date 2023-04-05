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
from django.urls import path, re_path
from museum_srv.views.video_stand_views import VideoStandPageAPIView, VideoStandEmployeeListAPIView, \
    VideoStandEmployeeAPIView
from museum_srv.views.timeline_views import TimeLineYearAPIView, TimeLineVideoAPIView
from museum_srv.views.area_samara_views import AreaSamaraStageAPIView, AreaSamaraVideoAPIView, \
    AreaSamaraAutoPlayAPIView
from museum_srv.views.technologies_views import TechnologiesStageAPIView, TechnologiesVideoLabelAPIView, \
    TechnologiesFourthAPIView, TechnologiesMovingAndBackstageAPIView
from museum_srv.views.flow_mask_views import FlowMaskAPIView, WholeMaskAPIView
from museum_srv.views.entry_group_views import EntryGroupVideoAPIView
from museum_srv.views.idle_views import IdleAPIView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video_stand/', VideoStandPageAPIView.as_view()),
    path('api/video_stand/page/', VideoStandPageAPIView.as_view()),
    path('api/video_stand/employee_list/<group>/', VideoStandEmployeeListAPIView.as_view()),
    path('api/video_stand/employee_list/', VideoStandEmployeeListAPIView.as_view()),
    path('api/video_stand/employee/', VideoStandEmployeeAPIView.as_view()),
    path('api/timeline/year/', TimeLineYearAPIView.as_view()),
    path('api/timeline/<year>/<int:video_index>/', TimeLineVideoAPIView.as_view()),
    path('api/area_samara/stage/', AreaSamaraStageAPIView.as_view()),
    path('api/area_samara/<int:stage>/video/', AreaSamaraVideoAPIView.as_view()),
    path('api/area_samara/auto_play/', AreaSamaraAutoPlayAPIView.as_view()),
    path('api/technologies/stage/', TechnologiesStageAPIView.as_view()),
    path('api/technologies/video_label/', TechnologiesVideoLabelAPIView.as_view()),
    path('api/technologies/fourth_video/<label>/', TechnologiesFourthAPIView.as_view()),
    path('api/technologies/<video_type>/<stage>/', TechnologiesMovingAndBackstageAPIView.as_view()),
    path('api/flows/', FlowMaskAPIView.as_view()),
    path('api/flows/<mask>/', WholeMaskAPIView.as_view()),
    path('api/entry_group/video/', EntryGroupVideoAPIView.as_view()),
    path('api/idle/<app>/', IdleAPIView.as_view()),
    path('api/idle/<app>/<field>/', IdleAPIView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
