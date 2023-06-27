import json
from dataclasses import dataclass
import requests
import time
from typing import Callable

from datetime import datetime

from museum_srv.modules.network import network_get

motor_url = 'http://192.168.1.136:1880/motor'

handle_technology_action: Callable or None = None


@dataclass
class MotorData:
    pos: int
    speed: int
    feed: int
    swn: int
    motor: bool
    esw1: bool
    esw2: bool
    esw3: bool
    esw4: bool
    esw5: bool
    pwr: bool
    res: bool

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        for field in ["motor", "pwr", "res", "esw1", "esw2", "esw3", "esw4", "esw5"]:
            data[field] = bool(data[field])
        return MotorData(**data)

    def to_json(self):
        return json.dumps(self.__dict__)


def set_handle_technology_action(action: Callable):
    # Need to set this instead of calling model method directly because of circular imports
    global handle_technology_action
    handle_technology_action = action


def listen_technology():
    # listen(technology_address, 'RD,ALL', handle_technology, 'technology stage', .3, True)
    while True:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        try:
            state_binary = network_get(motor_url + '?X')
            state_string = state_binary.decode('utf-8')
            motor_data = MotorData.from_json(state_string)
            handle_technology(motor_data)
        except requests.exceptions.ConnectionError:
            print(f'[{current_time}] Error while getting technology - timeout')
            time.sleep(3)
        except Exception as e:
            print(f'[{current_time}] UNKNOWN Error while getting technology: {e}')
            time.sleep(.05)
        time.sleep(5)


def handle_technology(response: MotorData):
    """
    :param response: string like this: #RD,110010
    """

    # create dictionary
    stages_dict = {
        'past': response.esw1,
        'present_1': response.esw2,
        'present_2': response.esw3,
        'present_3': response.esw4,
        'future': response.esw5,
    }

    stage = None

    # only one can be true
    if sum(stages_dict.values()) > 1:
        current_time = datetime.now().strftime("%H:%M:%S.%f'")
        raise Exception(f'[{current_time}] More than one stage is active: {stages_dict}')
    if sum(stages_dict.values()) == 1:
        # get first true value
        stage = list(stages_dict.keys())[list(stages_dict.values()).index(True)]

    global handle_technology_action
    if callable(handle_technology_action):
        handle_technology_action(stage)


def change_technology_move(state: str):
    """
    :param state: string like this: 'left', 'right', 'stop'
    """
    url = motor_url
    if state == 'left':
        url = url + '?R'
    elif state == 'right':
        url = url + '?F'
    elif state == 'stop':
        url = url + '?S'

    current_time = datetime.now().strftime("%H:%M:%S.%f'")
    try:
        resp = network_get(url)
        print(f'[{current_time}] Technology move sent {url} -> {resp}')
    except requests.exceptions.ConnectionError:
        print(f'[{current_time}] Error sending technology move - timeout')
    except Exception as e:
        print(f'[{current_time}] UNKNOWN Error sending technology move: {e}')
