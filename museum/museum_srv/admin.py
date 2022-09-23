from django.contrib import admin
from .models import VideoStandEmployee, TimeLine, AreaSamara, Technologies, TechnologiesMoving

admin.site.disable_action('delete_selected')
admin.site.register(VideoStandEmployee)
admin.site.register(TimeLine)
admin.site.register(AreaSamara)
admin.site.register(Technologies)
admin.site.register(TechnologiesMoving)


# @admin.register(VideoStandEmployee)
# class MyModelAdmin(admin.ModelAdmin):
#     def has_delete_permission(self, request, obj=None):
#         return False
#
# the example of deleting 'delete' button from the admin panel

