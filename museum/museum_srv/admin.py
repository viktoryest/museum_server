from django.contrib import admin
from museum_srv.models.video_stand_models import VideoStandEmployee
from museum_srv.models.timeline_models import TimeLine
from museum_srv.models.area_samara_models import AreaSamara
from museum_srv.models.technologies_models import Technologies, TechnologiesFourth
from museum_srv.models.entry_group_models import EntryGroupVideo
from museum_srv.models.idle_models import Idle

admin.site.disable_action('delete_selected')
admin.site.register(VideoStandEmployee)


@admin.register(TimeLine)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['year', 'video_1_duration', 'video_2_duration', 'intro_video_1_duration',
                       'intro_video_2_duration']
    exclude = ['video_2', 'intro_video_1', 'intro_video_2']


@admin.register(AreaSamara)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['stage', 'video_duration']


@admin.register(Technologies)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['stage', 'backstage_video_duration', 'moving_video_duration']


@admin.register(TechnologiesFourth)
class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ['fourth_stage_video_duration']


@admin.register(EntryGroupVideo)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['video_duration']


@admin.register(Idle)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['app', 'state', 'video_duration']
