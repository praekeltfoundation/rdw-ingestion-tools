from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("AAQ_API_KEY")
BASE_URL = config_from_env("AAQ_API_BASE_URL")


def get_paginated(
    client: Client,
    url: str,
    limit: int = 100,
    offset: int = 0,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Paginate over pages in an AAQ endpoint up to a limit."""

    params = {"offset": offset, "limit": limit}

    while True:
        print(
            "Retrieving results for offsets: ",
            params["offset"],
            "to",
            params["offset"] + limit,
            sep=" ",
        )
        # Need {**params, **kwargs}. mypy dislikes str|int for lines 29, 41.
        response = client.get(url, params={**params, **kwargs})
        response.raise_for_status()

        result: list[dict] = response.json()["result"]
        yield from result

        if len(result) < limit:
            return
        else:
            params["offset"] += limit


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}


client: Client = Client(base_url=BASE_URL, headers=headers)

from .main import pyAAQ as pyAAQ
