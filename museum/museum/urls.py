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
from museum_srv.views import VideoStandPageAPIView, VideoStandEmployeeListAPIView, TimeLineAPIView, \
    TimeLineVideoAPIView, \
    AreaSamaraAPIView, AreaSamaraVideoAPIView, TechnologiesStageAPIView, \
    TechnologiesVideoLabelAPIView, FlowMaskAPIView, VideoStandEmployeeAPIView, TechnologiesForthAPIView, \
    TechnologiesMovingAPIView, TechnologiesBackstageAPIView
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
    path('api/video_stand/employee/', VideoStandEmployeeAPIView.as_view()),
    path('api/timeline/year/', TimeLineAPIView.as_view()),
    path('api/timeline/<int:year>/<int:video>/', TimeLineVideoAPIView.as_view()),
    path('api/area_samara/pipeline/', AreaSamaraAPIView.as_view()),
    path('api/area_samara/video/', AreaSamaraVideoAPIView.as_view()),
    path('api/technologies/stage/', TechnologiesStageAPIView.as_view()),
    path('api/technologies/video_label/', TechnologiesVideoLabelAPIView.as_view()),
    path('api/technologies/fourth_video/<label>/', TechnologiesForthAPIView.as_view()),
    path('api/technologies/moving_video/<stage>/', TechnologiesMovingAPIView.as_view()),
    path('api/technologies/backstage_video/<stage>/', TechnologiesBackstageAPIView.as_view()),
    path('api/flows/', FlowMaskAPIView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
