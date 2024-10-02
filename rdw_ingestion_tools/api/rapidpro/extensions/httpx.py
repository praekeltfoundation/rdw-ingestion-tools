from collections.abc import Iterator

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

    while True:
        response = client.get(url, params={**kwargs})
        response.raise_for_status()

        data: dict = response.json()

        results: list = data["results"]
        yield from results

        try:
            url = data["next"].split("/v2/")[1]
        except AttributeError:
            break
