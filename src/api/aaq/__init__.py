from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


def paginate_get(
    httpx_client: Client, url: str, limit: int = 100, **kwargs
) -> list[dict]:
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
        response = httpx_client.get(url, params=params)
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


httpx_client = Client(base_url=BASE_URL, headers=headers)

from .main import pyAAQ as pyAAQ
