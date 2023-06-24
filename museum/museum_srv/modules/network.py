import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def network_get(url: str):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    req = requests.get(url, timeout=2)
    res = req.content
    return res
