import os
from urllib.parse import urljoin

from requests import Session

BASE_URL = "https://rapidpro.prd.momconnect.co.za/api/v2/"


class APIKeyMissingError(Exception):
    pass


try:
    API_KEY = os.environ["RAPIDPRO_API_KEY"]
except KeyError:
    raise APIKeyMissingError("Unable to locate API_KEY in the global environment.")

if not API_KEY:
    raise APIKeyMissingError("Unable to locate API_KEY in the global environment.")


class Session(Session):
    def __init__(self, url_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        url = urljoin(self.url_base, url)
        return super().request(method, url, **kwargs)

    def get(self, url, **kwargs):
        response = self.request(method="GET", url=url, **kwargs)
        l = []
        if response.ok:
            r = response.json()
            l.append(r["results"])
            try:
                next = r["next"]
            except KeyError:
                next = False
            while next:
                response = self.request(method="GET", url=next.split("/v2/")[1])
                if response.ok:
                    r = response.json()
                    l.append(r["results"])
                    try:
                        print(r["next"])
                        next = r["next"]
                    except KeyError:
                        next = False
                else:
                    raise Exception("Pagination response was not ok for request:", next)
        return l


session = Session(url_base=BASE_URL)
session.params = {}
session.headers = {}
session.headers = {"Authorization": f"Token {API_KEY}"}

from .main import pyRapid
