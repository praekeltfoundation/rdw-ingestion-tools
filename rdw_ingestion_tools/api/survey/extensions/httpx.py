from collections.abc import Iterator

from httpx import Client


def get_paginated(
    client: Client, url: str, start: str, max_pages: int, **kwargs: str | int
) -> Iterator[dict]:
    """Paginates over the custom MQR Survey API endpoint."""
    pages = 0

    params = {"updated_at_gt": start, **kwargs}

    while url and pages < max_pages:
        response = client.get(url=url, params=params)
        response.raise_for_status()

        data: list[dict] = response.json()["results"]

        yield from data

        url = response.json()["next"]

        pages += 1
