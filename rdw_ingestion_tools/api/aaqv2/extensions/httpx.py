from collections.abc import Iterator

from httpx import Client


def get(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Get data from an AAQV2 endpoint.

    NOTE: This new API doesn't support pagination like the previous API did :/
    Consider opening a PR to their repo for this?

    """

    response = client.get(url, params={**kwargs})
    response.raise_for_status()

    result: list[dict] = response.json()
    yield from result
