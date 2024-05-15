from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


class BaseClient(Client):
    """To be used in various enpoint specific requests.

    Need to subclass here in order to overload `paginate_get` which is useful
    for each of the different endpoint specific request in this submodule.

    """

    def __init__(self, *args, **kwargs) -> Client:
        super().__init__(*args, **kwargs)

    def paginate_get(self, url: str, limit: int = 100, **kwargs) -> list[dict]:
        """Paginate over pages in an AAQ endpoint up to a limit."""
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
            response = self.get(url, params=params)
            response.raise_for_status()
            result = response.json()["result"]
            response_list.append(result)
            if len(result) == params["limit"]:
                params["offset"] += params["limit"]
            elif len(result) < params["limit"]:
                break

        response_list = sum(response_list, [])

        return response_list


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

base_client = BaseClient(base_url=BASE_URL, headers=headers)

from .main import pyAAQ as pyAAQ
