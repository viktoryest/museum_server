from django.contrib import admin
from .models import VideoStandEmployee

admin.site.disable_action('delete_selected')
admin.site.register(VideoStandEmployee)


# @admin.register(VideoStandEmployee)
# class MyModelAdmin(admin.ModelAdmin):
#     def has_delete_permission(self, request, obj=None):
#         return False
#
# the example of deleting 'delete' button from the admin panel

