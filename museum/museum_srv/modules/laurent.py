from typing import Callable

import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from exceptions import LaurentException
from datetime import datetime

flows_address = 'http://192.168.1.3'
technology_address = 'http://192.168.1.5'


def get_laurent(address: str, command: str):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    url = get_url(address, command)
    laurent_request = requests.get(url, timeout=2)
    laurent_response = laurent_request.content
    return laurent_response


def get_url(address: str, command: str):
    url = f'{address}/cmd.cgi?psw=Laurent&cmd={command}'
    return url


def listen(address: str, command: str, action: Callable, debug_name: str, sleep_time: int = 1):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        try:
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


handle_technology_action: Callable or None = None


def set_handle_technology_action(action: Callable):
    # Need to set this instead of calling model method directly because of circular imports

    global handle_technology_action
    handle_technology_action = action


def handle_technology(response):
    """
    :param response: string like this: #RD,110010
    """

    # remove first '#RD,' and last '/r/n'
    print(response)
    laurent_mask = response[4:10].decode('utf-8')
    print(laurent_mask)
    # create dictionary
    stages_dict = {
        'past': laurent_mask[0] == '0',
        'present_1': laurent_mask[2] == '1',
        'present_2': laurent_mask[3] == '1',
        'present_3': laurent_mask[4] == '1',
        'future': laurent_mask[5] == '0',
    }

    print(stages_dict)
    print("sum: ", sum(stages_dict.values()))
    print("number of true", list(stages_dict.values()).count(True))

    stage = None

    # only one can be true
    if sum(stages_dict.values()) > 1:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        raise Exception(f'[{current_time}] More than one stage is active: {stages_dict}')
    if sum(stages_dict.values()) == 1:
        # get first true value
        stage = list(stages_dict.keys())[list(stages_dict.values()).index(True)]

    print("stage: ", stage)
    print("handle_technology_action: ", handle_technology_action, callable(handle_technology_action))
    if callable(handle_technology_action):
        handle_technology_action(stage)


def listen_technology():
    listen(technology_address, 'RD,ALL', handle_technology, 'technology stage', 10)


def change_technology_move(state: str):
    """
    :param state: string like this: 'left', 'right', 'stop'
    """
    command = "REL,ALL,xx"
    if state == 'left':
        command = command + '10'
    elif state == 'right':
        command = command + '01'
    elif state == 'stop':
        command = command + '00'
    else:
        raise Exception(f'Unknown state: {state}, should be "left", "right" or "stop"')

    current_time = datetime.now().strftime("%H:%M:%S.%f'")
    try:
        url = get_url(technology_address, command)
        print(f'[{current_time}] Technology move sent to laurent: {state}, url: {url}')
        resp = get_laurent(technology_address, command)
        print(f'[{current_time}] Technology response: {resp}')
    except LaurentException:
        print(f'[{current_time}] Error sending technology move to laurent')
    except requests.exceptions.ConnectionError:
        print(f'[{current_time}] Error sending technology move to laurent - timeout')
    except Exception as e:
        print(f'[{current_time}] UNKNOWN Error sending technology move to laurent: {e}')
