import os
from urllib.parse import urljoin

from requests import Session

BASE_URL = "https://whatsapp.praekelt.org/v1/data/"


class APIKeyMissingError(Exception):
    pass


try:
    API_KEY = os.environ["TURN_API_KEY"]
except KeyError:
    raise APIKeyMissingError(
        "Unable to locate API_KEY in the global environment."
    )

if not API_KEY:
    raise APIKeyMissingError(
        "Unable to locate API_KEY in the global environment."
    )


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
session.headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

from .main import pyTurn