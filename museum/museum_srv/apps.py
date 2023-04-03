from django.apps import AppConfig
from django.db.models.signals import post_migrate


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


def setDaemon(self, daemonic: bool) -> None:
    import threading

    t = threading.Thread(target=listen_to_laurant_flows)
    t.start()


def listen_to_laurant_flows():
    import requests
    import time
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from museum_srv.views import WholeMaskAPIView

    while True:
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            laurant_request = requests.get('http://192.168.1.3/cmd.cgi?psw=Laurent&cmd=RID,ALL')
            laurant_response = laurant_request.content
            new_mask = laurant_response[5:12]
            new_mask = new_mask[::-1]
            WholeMaskAPIView.post(self=WholeMaskAPIView, request=None, mask=new_mask)
            print(f'Flows mask from laurent: {new_mask}')
        except Exception as e:
            print(f'Error while getting flows mask from laurent: {e}')
        time.sleep(0.3)


class MuseumSrvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'museum_srv'

    def ready(self):
        post_migrate.connect(create_default_tables, sender=self)
        setDaemon(self, True)
