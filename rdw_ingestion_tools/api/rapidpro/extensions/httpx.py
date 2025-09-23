from collections.abc import Iterator
from urllib.parse import unquote

from httpx import Client


def get_paginated(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Paginate over a Rapidpro API endpoint.

    The Rapidpro API returns a next token with each response until no further
    pages are left to return.

    """
    params = {**kwargs}

    while True:
        response = client.get(url, params=params)
        response.raise_for_status()

        data: dict = response.json()

        results: list = data["results"]
        yield from results

        try:
            cursor = data["next"].split("cursor=")[1].split("&")[0]
            decoded_cursor = unquote(cursor)
            params["cursor"] = decoded_cursor
        except AttributeError:
            break
