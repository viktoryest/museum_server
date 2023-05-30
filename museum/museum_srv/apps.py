from django.apps import AppConfig
from django.db.models.signals import post_migrate

from museum_srv.modules.laurent import listen_flows, listen_technology


def create_default_tables(sender, **kwargs):
    """Creates tables with default values after migrations"""
    from museum_srv.models.timeline_models import TimeLine
    from museum_srv.models.flow_mask_models import FlowMask
    from museum_srv.models.area_samara_models import AreaSamara, AreaSamaraAutoPlay
    from museum_srv.models.technologies_models import Technologies
    from museum_srv.models.entry_group_models import EntryGroupVideo
    from museum_srv.models.idle_models import Idle

    TimeLine.check_timeline_videos()
    FlowMask.check_flows()
    AreaSamara.check_area_samara_stages()
    AreaSamaraAutoPlay.check_area_samara_auto_play()
    Technologies.check_technologies_stages()
    EntryGroupVideo.check_entry_group_video()
    Idle.check_idle_videos()


def set_daemons(self, daemonic: bool) -> None:
    import threading

    t = threading.Thread(target=listen_flows, daemon=True)
    t.start()

    t = threading.Thread(target=listen_technology, daemon=True)
    t.start()


class MuseumSrvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'museum_srv'

    def ready(self):
        from museum_srv.models.technologies_models import TechnologiesLaurent
        post_migrate.connect(create_default_tables, sender=self)
        TechnologiesLaurent.subscribe_events()
        set_daemons(self, True)
