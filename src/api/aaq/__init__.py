from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


def get_paginated(
    client: Client, url: str, limit: int = 100, offset: int = 0, **kwargs
) -> list[dict]:
    """Paginate over pages in an AAQ endpoint up to a limit."""

    params = {"offset": offset, "limit": limit, **kwargs}

    response_list = []

    while True:
        print(
            "Retrieving results for offsets: ",
            params["offset"],
            "to",
            params["offset"] + params["limit"],
            sep=" ",
        )
        response = client.get(url, params=params)
        response.raise_for_status()
        result = response.json()["result"]
        response_list.extend(result)
        if len(result) < limit:
            break
        else:
            params["offset"] += limit


    response_list = [{k: str(v) for k, v in d.items()} for d in response_list]

    return response_list


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}


client = Client(base_url=BASE_URL, headers=headers)

from .main import pyAAQ as pyAAQ
