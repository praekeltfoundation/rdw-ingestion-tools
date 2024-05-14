from urllib.parse import urljoin

from requests import Session

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


class Session(Session):
    def __init__(self, url_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        url = urljoin(self.url_base, url)
        return super().request(method, url, **kwargs)

    def get(self, url, **kwargs):
        params = {**kwargs}

        params["offset"] = 0
        if "limit" not in params:
            params["limit"] = 100

        response_list = []

        while True:
            print(
                "Retrieving results for offsets: ",
                params["offset"],
                "to",
                params["offset"] + params["limit"],
                sep=" ",
            )
            response = self.request("GET", url, params=params)
            response.raise_for_status()
            result = response.json()["result"]
            response_list.append(result)
            if len(result) == params["limit"]:
                params["offset"] += params["limit"]
            elif len(result) < params["limit"]:
                break

        response_list = sum(response_list, [])

        return response_list


session = Session(url_base=BASE_URL)
session.params = {}
session.headers = {}
session.headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

from .main import pyAAQ as pyAAQ
