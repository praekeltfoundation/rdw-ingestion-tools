from urllib.parse import urljoin

from attrs import define
from requests import Response, Session

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


@define
class BaseSession(Session):
    """Base requests session to use in requests to different API endpoints in
    the module.

    Args:
       url_base: The base url to reference (str) (This has to be str | bytes in
       accordance with what requests accepts?)
       *args
       **kwargs
    """

    url_base: str

    # TODO: attrs doesn't like subclassing.
    def __attrs_post_init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> Response:
        """Send request to an API endpoint by providing only the endpoint with
        the base url as part of initialisation.

        Args:
           method: The method type. aGET, PUT etc. (str)
           url: The endpoint. (str)
           **kwargs

        Returns:
           requests.Response
        """
        url = urljoin(self.url_base, url)
        return super().request(method, url, **kwargs)

    def get(self, url: str, limit: int = 100, **kwargs) -> list[dict]:
        """Paginate over pages in an AAQ endpoint up to a limit.

        Args:
           url: the endpoint. (str)
           limit: The limit of pages to paginate over. (int)

        Returns:
           list[Response]
        """
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


base_session = BaseSession(url_base=BASE_URL)
base_session.params = {}
base_session.headers = {}
base_session.headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

from .main import pyAAQ as pyAAQ
