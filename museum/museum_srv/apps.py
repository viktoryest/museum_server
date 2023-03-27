from django.apps import AppConfig
from django.conf import settings
from django.core.signals import setting_changed, request_finished
from django.db.models.signals import post_migrate, post_init


def create_default_tables(sender, **kwargs):
    """Creates tables with default values after migrations"""
    from museum_srv.models import TimeLine, FlowMask, AreaSamara, AreaSamaraAutoPlay, Technologies, EntryGroupVideo, \
        Idle

    TimeLine.check_timeline_videos()
    FlowMask.check_flows()
    AreaSamara.check_area_samara_stages()
    AreaSamaraAutoPlay.check_area_samara_auto_play()
    Technologies.check_technologies_stages()
    EntryGroupVideo.check_entry_group_video()
    Idle.check_idle_videos()


class MuseumSrvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'museum_srv'

    def ready(self):
        post_migrate.connect(create_default_tables, sender=self)
