from django.apps import AppConfig
from django.db.models.signals import post_migrate
from exceptions import LaurantException


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


def setDaemon(self, daemonic: bool) -> None:
    import threading

    t = threading.Thread(target=listen_to_laurant_flows, daemon=True)
    t.start()


def listen_to_laurant_flows():
    import requests
    import time
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from museum_srv.views.flow_mask_views import WholeMaskAPIView, FlowMaskAPIView

    while True:
        try:
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            # add timeout
            laurant_request = requests.get('http://192.168.1.3/cmd.cgi?psw=Laurent&cmd=RID,ALL', timeout=1)
            laurant_response = laurant_request.content
            laurant_mask = laurant_response[5:12]
            reverted_mask = laurant_mask[::-1]
            new_mask = str(reverted_mask)[2:9].zfill(7)
            current_mask_response = FlowMaskAPIView.get(self=FlowMaskAPIView, request=None)
            current_mask = current_mask_response.data['mask']
            if current_mask != new_mask:
                WholeMaskAPIView.post(self=WholeMaskAPIView, request=None, mask=new_mask)
                print(f'Flows mask from laurent: {new_mask}')
        except LaurantException:
            print(f'Error while getting flows mask from laurent')
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            print(f'Error while getting flows mask from laurent - timeout')
            time.sleep(1)
        except Exception as e:
            print(f'UNKNOWN Error while getting flows mask from laurent: {e}')
        time.sleep(0.5)


class MuseumSrvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'museum_srv'

    def ready(self):
        post_migrate.connect(create_default_tables, sender=self)
        setDaemon(self, True)
