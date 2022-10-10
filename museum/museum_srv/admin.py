from django.contrib import admin
from .models import VideoStandEmployee, TimeLine, AreaSamara, Technologies, FlowMask, TechnologiesFourth

admin.site.disable_action('delete_selected')
admin.site.register(VideoStandEmployee)
admin.site.register(AreaSamara)
admin.site.register(Technologies)
admin.site.register(TechnologiesFourth)
admin.site.register(FlowMask)


@admin.register(TimeLine)
class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    readonly_fields = ['year', 'video_1_duration', 'video_2_duration']
