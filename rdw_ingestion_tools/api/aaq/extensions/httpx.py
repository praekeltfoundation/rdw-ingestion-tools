from collections.abc import Iterator

from httpx import Client


def get_paginated(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Paginate over pages in an AAQ endpoint up to a limit."""

    limit: int = 100
    offset: int = 0

    params = {"offset": offset, "limit": limit}

    while True:
        print(
            "Retrieving results for offsets: ",
            params["offset"],
            "to",
            params["offset"] + limit,
            sep=" ",
        )
        # Need {**params, **kwargs}. mypy dislikes str|int for lines 27, 40.
        response = client.get(url, params={**params, **kwargs})
        response.raise_for_status()

        result: list[dict] = response.json()["result"]
        yield from result

        if len(result) < limit:
            return
        else:
            params["offset"] += limit
