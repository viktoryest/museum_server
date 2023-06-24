from typing import Callable

import requests
import time

from exceptions import LaurentException
from datetime import datetime

from museum_srv.modules.network import network_get

flows_address = 'http://192.168.1.3'
technology_address = 'http://192.168.1.5'


def get_laurent(address: str, command: str):
    url = get_url(address, command)
    return network_get(url)


def get_url(address: str, command: str):
    url = f'{address}/cmd.cgi?psw=Laurent&cmd={command}'
    return url


def listen(address: str, command: str, action: Callable, debug_name: str, sleep_time: float = 1, debug: bool = False):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        try:
            if debug:
                # read from file
                with open('laurent_response.txt', 'r') as file:
                    laurent_response = file.read().encode('utf-8')
            else:
                laurent_response = get_laurent(address, command)
            action(laurent_response)
        except LaurentException:
            print(f'[{current_time}] Error while getting {debug_name} from laurent')
            time.sleep(3)
        except requests.exceptions.ConnectionError:
            print(f'[{current_time}] Error while getting {debug_name} from laurent - timeout')
            time.sleep(3)
        except Exception as e:
            print(f'[{current_time}] UNKNOWN Error while getting {debug_name} from laurent: {e}')
            time.sleep(10)
        time.sleep(sleep_time)


def handle_flows(response: str):
    """
    :param response: string like this: #RID,100100000000
    """
    from museum_srv.views.flow_mask_views import WholeMaskAPIView, FlowMaskAPIView
    # remove first '#RID,' and last '/r/n'
    laurent_mask = response[5:12]
    reverted_mask = laurent_mask[::-1]
    new_mask = str(reverted_mask)[2:9].zfill(7)
    current_mask_response = FlowMaskAPIView.get(self=FlowMaskAPIView, request=None)
    current_mask = current_mask_response.data['mask']
    if current_mask != new_mask:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        WholeMaskAPIView.post(self=WholeMaskAPIView, request=None, mask=new_mask)
        print(f'[{current_time}] Flows mask from laurent: {new_mask}')


def listen_flows():
    listen(flows_address, 'RID,ALL', handle_flows, 'flows mask')
