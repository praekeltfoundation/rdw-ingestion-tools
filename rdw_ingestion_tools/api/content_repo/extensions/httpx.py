from collections.abc import Iterator

from httpx import Client


def get_paginated(
    client: Client, url: str, max_pages: int, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over a Content Repo API endpoint."""
    pages = 0

    while url and pages < max_pages:
        response = client.get(url, follow_redirects=True, params={**kwargs})
        response.raise_for_status()

        data: dict = response.json()

        results: dict = data["results"]
        yield from results

        url = data["next"]

        pages += 1
