from urllib.parse import urljoin

from requests import Session

from .. import config_from_env

API_KEY = config_from_env("RAPIDPRO_API_KEY")
BASE_URL = config_from_env("RAPIDPRO_API_BASE_URL")


class Session(Session):
    def __init__(self, url_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        url = urljoin(self.url_base, url)
        return super().request(method, url, **kwargs)

    def get(self, url, **kwargs):
        response = self.request(method="GET", url=url, **kwargs)
        response.raise_for_status()
        response_list = []
        if response.ok:
            r = response.json()
            response_list.append(r["results"])
            try:
                next = r["next"]
            except KeyError:
                next = False
            while next:
                response = self.request(
                    method="GET", url=next.split("/v2/")[1]
                )
                if response.ok:
                    r = response.json()
                    response_list.append(r["results"])
                    try:
                        print(r["next"])
                        next = r["next"]
                    except KeyError:
                        next = False
                else:
                    raise Exception(
                        "Pagination response was not ok for request:", next
                    )
        return response_list


session = Session(url_base=BASE_URL)
session.params = {}
session.headers = {}
session.headers = {"Authorization": f"Token {API_KEY}"}

from .main import pyRapid as pyRapid
