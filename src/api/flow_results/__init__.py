from urllib.parse import urljoin

from requests import Session

from .. import config_from_env

API_KEY = config_from_env("FLOW_RESULTS_API_KEY")
BASE_URL = config_from_env("FLOW_RESULTS_API_BASE_URL")


class Session(Session):
    def __init__(self, url_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        url = urljoin(self.url_base, url)
        return super().request(method, url, **kwargs)


session = Session(url_base=BASE_URL)
session.params = {}
session.headers = {}
session.headers = {"Authorization": f"Token {API_KEY}"}

from .main import pyFlows as pyFlows
