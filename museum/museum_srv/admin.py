from django.contrib import admin
from .models import VideoStandEmployee, TimeLine, AreaSamara, Technologies, FlowMask, TechnologiesFourth, \
    EntryGroupVideo

admin.site.disable_action('delete_selected')
admin.site.register(VideoStandEmployee)


@admin.register(TimeLine)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['year', 'video_1_duration', 'video_2_duration']


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
